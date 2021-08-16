package yourway.job;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.Optional;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaInputDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import scala.Tuple2;
import settings.Settings;

import java.lang.reflect.Type;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public final class UserQuery {

    public static void main(String[] args) throws Exception {
        Type type = new TypeToken<Map<String, Object>>() {}.getType();
        Function2<List<Map<String, Object>>, Optional<Map<String, Object>>, Optional<Map<String, Object>>> updateFunction =
                (maps, hashMapOptional) -> hashMapOptional;
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("Storing User Query");
        JavaStreamingContext streamingContext = new JavaStreamingContext(conf, Durations.seconds(1));
        try {
            streamingContext.sparkContext().setLogLevel("ERROR");
            streamingContext.checkpoint(Settings.CHECKPOINT_PATH);

            Map<String, Object> kafkaParams = new HashMap<>();
            kafkaParams.put("bootstrap.servers", Settings.KAFKA_URI);
            kafkaParams.put("key.deserializer", StringDeserializer.class);
            kafkaParams.put("value.deserializer", StringDeserializer.class);
            kafkaParams.put("group.id", "group_user_query");
            JavaInputDStream<ConsumerRecord<String, String>> inputKafka = KafkaUtils.createDirectStream(
                    streamingContext,
                    LocationStrategies.PreferConsistent(),
                    ConsumerStrategies.Subscribe(Collections.singleton(Settings.TOPIC_SET_USER_QUERY),
                            kafkaParams)
            );

            JavaPairDStream<String, Map<String, Object>> results = inputKafka.mapToPair(
                    record -> new Tuple2<>(record.key(), (new Gson()).fromJson(record.value(), type))
            );
            results.print(5);
            JavaPairDStream<Object, Map<String, Object>> userQuery = results.mapToPair(
                    s -> new Tuple2<>(s._2.get("id"), s._2)
            ).updateStateByKey(updateFunction);

            userQuery.print(5);
            streamingContext.start();
            streamingContext.awaitTermination();
            streamingContext.close();
            streamingContext.sparkContext().close();
            System.out.println("finish program!");
        } catch (IllegalStateException | NoSuchMethodError e) {
            System.out.println(e.getMessage());
        } finally {
            streamingContext.close();
            streamingContext.sparkContext().close();
        }
    }
}

