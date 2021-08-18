package yourway;

import org.apache.spark.sql.Column;
import org.apache.spark.sql.Dataset;
import org.apache.spark.sql.Row;
import org.apache.spark.sql.SparkSession;
import org.apache.spark.sql.api.java.UDF1;
import org.apache.spark.sql.expressions.UserDefinedFunction;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.types.DataTypes;
import org.apache.spark.sql.functions.*;
import settings.Settings;

import static org.apache.spark.sql.functions.*;

public class WarningJob {

    public static void main(String[] args) {
        SparkSession spark = SparkSession
                .builder()
                .appName("Warning Job Yourway")
                .getOrCreate();

        Dataset<Row> df = spark
                .readStream()
                .format("kafka")
                .option("kafka.bootstrap.servers", Settings.KAFKA_URI)
                .option("subscribe", Settings.TOPIC_JOB)
                .load();

        UserDefinedFunction decode_string = udf((UDF1<Byte, Object>) Object::toString, DataTypes.StringType);

//        Dataset<Row> data = df.select(
//                    json_tuple(
//                            udf((Byte x) -> x, DataTypes.StringType),
//                            "id"
//            ).alias("id")
//        );

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

//        StreamingQuery ds = df
//                .writeStream()
//                .format("kafka")
//                .option("kafka.bootstrap.servers", Settings.KAFKA_URI)
//                .option("topic", Settings.TOPIC_USER)
//                .start();
//
//        ds.awaitTermination();
    }

}
