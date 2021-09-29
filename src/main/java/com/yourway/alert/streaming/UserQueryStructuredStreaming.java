package com.yourway.alert.streaming;

import com.yourway.alert.streaming.settings.Database;
import com.yourway.alert.streaming.settings.Settings;
import org.apache.spark.TaskContext;
import org.apache.spark.api.java.function.MapFunction;
import org.apache.spark.api.java.function.MapGroupsWithStateFunction;
import org.apache.spark.sql.*;
import org.apache.spark.sql.streaming.OutputMode;
import org.apache.spark.sql.streaming.StreamingQuery;
import org.apache.spark.sql.streaming.StreamingQueryException;
import scala.collection.JavaConverters;
import scala.collection.Seq;

import java.util.concurrent.TimeoutException;

import static org.apache.spark.sql.functions.col;
import static org.apache.spark.sql.functions.json_tuple;
import static org.apache.spark.sql.types.DataTypes.StringType;

public class UserQueryStructuredStreaming {

    public static void main(String[] args) throws TimeoutException, StreamingQueryException {
        SparkSession spark = SparkSession
            .builder()
            .appName("Yourway User Query Storage")
            .getOrCreate();
        spark.sparkContext().setLogLevel("ERROR");

        Dataset<Row> df_static = spark.read()
            .format("jdbc")
            .option("url", "jdbc:mysql://localhost:3306/yourway")
            .option("dbtable", "userquery")
            .option("user", Database.DB_USERNAME)
            .option("password", Database.DB_PASSWORD)
            .option("driver", "com.mysql.jdbc.Driver")
            .load();

        Dataset<Row> df_streaming = spark
            .readStream()
            .format("kafka")
            .option("kafka.bootstrap.servers", Settings.KAFKA_URI)
            .option("subscribe", Settings.TOPIC_SET_USER_QUERY)
            .load();

        df_static.show();
        df_streaming.printSchema();
        Seq<String> seq = JavaConverters.asScalaIteratorConverter(Settings.FIELD_QUERY.iterator()).asScala().toSeq();
        System.out.println(1);
        Dataset<Row> dataExtracted = df_streaming.select(
            json_tuple(
                col("value").cast(StringType), seq
            )
        );
        dataExtracted.show();
        KeyValueGroupedDataset<String, Row> kvDataset = dataExtracted.groupByKey(
            (MapFunction<Row, String>) value -> "value", Encoders.STRING()
        );
        System.out.println(2);

        //process
        Dataset<Row> data = kvDataset.mapGroupsWithState((MapGroupsWithStateFunction<String, Row, Row, Row>) (key, values, state) -> {
            System.out.println("CameraId=" + key + " PartitionId=" + TaskContext.getPartitionId());
            Row existing = null;
            //check previous state
            if (state.exists()) {
                existing = state.get();
            }
            //classify image
            Row processed = existing;

            //update last processed
            if (processed != null) {
                state.update(processed);
            }
            return processed;
        }, Encoders.bean(Row.class), Encoders.bean(Row.class));
        System.out.println(3);

        StreamingQuery ds = data
            .writeStream()
            .outputMode(OutputMode.Update())
            .format("console")
            .start();

        ds.awaitTermination();

    }
}
