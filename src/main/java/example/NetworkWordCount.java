package example;

import org.apache.spark.*;
import org.apache.spark.api.java.function.*;
import org.apache.spark.api.java.Optional;
import org.apache.spark.streaming.*;
import org.apache.spark.streaming.api.java.*;
import scala.Tuple2;
import settings.Settings;
import java.util.Arrays;
import java.util.List;

public final class NetworkWordCount {

    public static void main(String[] args) throws Exception {
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("NetworkWordCount");
        JavaStreamingContext jssc = new JavaStreamingContext(conf, Durations.seconds(1));
        jssc.sparkContext().setLogLevel("ERROR");
        jssc.checkpoint(Settings.CHECKPOINT_PATH);

        Function2<List<Integer>, Optional<Integer>, Optional<Integer>> updateFunction =
                (values, state) -> {
                    Integer newSum = state.or(0);
                    for (Integer i: values) {
                        newSum += i;
                    }
                    return Optional.of(newSum);
                };

        JavaReceiverInputDStream<String> lines = jssc.socketTextStream("localhost", 9999);
        JavaDStream<String> words = lines.flatMap(x -> Arrays.asList(x.split(" ")).iterator());
        JavaPairDStream<String, Integer> pairs = words.mapToPair(s -> new Tuple2<>(s, 1));
        JavaPairDStream<String, Integer> wordCounts = pairs.updateStateByKey(updateFunction);

        // Print the first ten elements of each RDD generated in this DStream to the console
        wordCounts.print();

        jssc.start();
        jssc.awaitTermination();
    }
}

