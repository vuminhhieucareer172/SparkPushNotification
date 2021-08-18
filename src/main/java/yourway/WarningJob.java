package yourway;

import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.ConsumerRecords;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.streaming.StreamingQueryException;
import scala.collection.Seq;
import settings.Settings;
import scala.collection.JavaConverters;

import java.util.Collections;
import java.util.Properties;
import java.util.concurrent.TimeoutException;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.json_tuple;
import static org.apache.spark.sql.types.DataTypes.StringType;

public class WarningJob {

    public static void main(String[] args) throws TimeoutException, StreamingQueryException {
        SparkSession spark = SparkSession
                .builder()
                .appName("Warning Job Yourway")
                .getOrCreate();
        spark.sparkContext().setLogLevel("ERROR");
        Dataset<Row> df = spark
                .readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", Settings.KAFKA_URI)
                .option("subscribe", Settings.TOPIC_JOB)
                .load();

        Seq<String> seq = JavaConverters.asScalaIteratorConverter(Settings.FIELD_JOB.iterator()).asScala().toSeq();


        Dataset<Row> data = df.select(
                json_tuple(
                        col("value").cast(StringType), seq
                )
        );

        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, Settings.KAFKA_URI);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, "user");
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);

        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(props);
        consumer.subscribe(Collections.singletonList(Settings.TOPIC_USER_QUERY));
        ConsumerRecords<String, String> records = consumer.poll(100);
        System.out.println(records);
        for (ConsumerRecord<String, String> record : records)
            System.out.printf("offset = %d, key = %s, value = %s%n", record.offset(), record.key(), record.value());

//        check_matching = udf(
//                lambda address, age, salary, year, edu_level, job_attribute: matching(address, age, salary, year, edu_level,
//                job_attribute), StringType()
//    )
//
//        data = data.withColumn(
//                "value", check_matching(data["company_address"], data["ages"], data["salary"], data["year_experiences"],
//                        data["education_level"], data["job_attribute"])
//        )
//        data = data.withColumn(
//                "key", col("id")
//        )
//
//        data = data.filter(col("value") != "")

        StreamingQuery ds = data
                .writeStream()
                .format("console")
                .start();

//        StreamingQuery ds = data
//                .writeStream()
//                .format("kafka")
//                .option("kafka.bootstrap.servers", Settings.KAFKA_URI)
//                .option("checkpointLocation", Settings.CHECKPOINT_PATH)
//                .option("topic", Settings.TOPIC_USER)
//                .start();

        ds.awaitTermination();
    }
}
