package yourway.streaming;

import org.apache.kafka.clients.consumer.ConsumerConfig;
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
import utils.UtilKafka;

import java.util.*;

public final class UserQuery {
    public static void main(String[] args) throws Exception {
        Function2<List<String>, Optional<String>, Optional<String>> updateFunction =
                (maps, hashMapOptional) -> {
                    String out;
                    if (hashMapOptional.isPresent()) {
                        out = hashMapOptional.get();
                    } else {
                        out = maps.get(maps.size() - 1);
                    }
                    return Optional.of(out);
                };
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("Storing User Query");
        JavaStreamingContext streamingContext = new JavaStreamingContext(conf, Durations.seconds(2));
        try {
            streamingContext.sparkContext().setLogLevel("ERROR");
//            streamingContext.sparkContext().broadcast();
            streamingContext.checkpoint(Settings.CHECKPOINT_PATH);

            Map<String, Object> kafkaParams = new HashMap<>();
            kafkaParams.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, Settings.KAFKA_URI);
            kafkaParams.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
            kafkaParams.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class);
            kafkaParams.put(ConsumerConfig.GROUP_ID_CONFIG, "group_user_query");
            JavaInputDStream<ConsumerRecord<String, String>> inputKafka = KafkaUtils.createDirectStream(
                    streamingContext,
                    LocationStrategies.PreferConsistent(),
                    ConsumerStrategies.Subscribe(Collections.singleton(Settings.TOPIC_SET_USER_QUERY),
                            kafkaParams)
            );
            Properties props = UtilKafka.createProducer("KafkaProducer");
            JavaPairDStream<String, String> results = inputKafka.mapToPair(
                    record -> new Tuple2<>(record.key(), record.value())
            );
            JavaPairDStream<String, String> newState = results.updateStateByKey(updateFunction);

            newState.print();

            UtilKafka.sendRDDToKafka(props, Settings.TOPIC_USER_QUERY, "userQuery", newState);

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
