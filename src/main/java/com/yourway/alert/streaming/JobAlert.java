package com.yourway.alert.streaming;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.yourway.alert.domain.Query;
import com.yourway.alert.streaming.settings.Settings;
import com.yourway.alert.utils.UtilKafka;
import org.apache.commons.lang3.math.NumberUtils;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.api.java.UDF6;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.streaming.StreamingQueryException;
import org.apache.spark.sql.types.DataTypes;
import scala.collection.JavaConverters;
import scala.collection.Seq;

import java.lang.reflect.Type;
import java.util.ArrayList;
import java.util.List;
import java.util.Objects;
import java.util.Properties;
import java.util.concurrent.TimeoutException;

import static org.apache.spark.sql.functions.*;
import static org.apache.spark.sql.types.DataTypes.StringType;

public class JobAlert {

    public static void main(String[] args) throws TimeoutException, StreamingQueryException {
        SparkSession spark = SparkSession
                .builder()
                .appName("Alert Job Yourway")
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
        data.printSchema();
        // get user query from kafka
        Properties props = UtilKafka.createConsumer("user");
        ConsumerRecord<String, String> mess = UtilKafka.getLatestMessage(props, Settings.TOPIC_USER_QUERY);
        Gson gson = new Gson();
        Type type = new TypeToken<ArrayList<Query>>() {
        }.getType();
        if (mess != null) {
            ArrayList<Query> listQuery = gson.fromJson(mess.value(), type);
            // matching
            try {
                UDF6<String, String, String, String, String, String, String> check_matching = (address, age, salary, yearExperiments, eduLevel, jobAttribute) -> {
                    List<String> user_id = new ArrayList<>();
                    int min_age = 0;
                    int max_age = 200;

                    if (age != null && !age.isEmpty()) {
                        String[] array_age = age.split(",");
                        if (array_age.length > 1) {
                            min_age = Settings.DICT_MIN_AGE.get(array_age[0]);
                            max_age = Settings.DICT_MAX_AGE.get(array_age[array_age.length - 1]);
                        }
                    }
                    for (Query query : listQuery) {
                        Long querySalary = query.getSalary();

                        boolean is_number_salary = true;
                        if (salary != null && !salary.isEmpty()) {
                            float salaryFloat = Float.parseFloat(salary);
                            is_number_salary = salaryFloat >= querySalary;
                        }
                        boolean is_not_none_address = false;
                        if (address != null && !address.isEmpty()) {
                            is_not_none_address = address.contains(query.getCompanyAddress());
                        }

                        try {
                            if (is_not_none_address && min_age <= query.getAge() && query.getAge() <= max_age &&
                                    is_number_salary && Objects.equals(query.getYearExperiences(), yearExperiments) &&
                                    Objects.equals(query.getEducationLevel(), eduLevel) &&
                                    Objects.equals(query.getJobAttribute(), jobAttribute)) {
                                user_id.add(String.valueOf(query.getUserId()));
                            }
                        } catch (Exception e) {
                            System.out.println(e.getMessage());
                        }
                    }
                    return String.join(",", user_id);
                };
                spark.sqlContext().udf().register("matching", check_matching, DataTypes.StringType);
                data = data.withColumn("value",
                        callUDF("matching",
                                col("c2"), col("c14"), col("c10"), col("c22"), col("c15"), col("c19")));
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        } else {
            data = data.withColumn("value", lit(null).cast(StringType));
        }

        data = data.withColumn(
                "key", col("c0")
        );
        data = data.filter(col("value").isNotNull());

        StreamingQuery ds = data
                .writeStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", Settings.KAFKA_URI)
                .option("kafka.group.id", Settings.GROUP_ID_USER)
                .option("checkpointLocation", Settings.CHECKPOINT_PATH)
                .option("topic", Settings.TOPIC_USER)
                .start();

        ds.awaitTermination();
    }
}
