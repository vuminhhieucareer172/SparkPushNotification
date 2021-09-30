package com.yourway.alert.streaming;

import com.google.gson.Gson;
import com.google.gson.reflect.TypeToken;
import com.yourway.alert.domain.JsonQuery;
import com.yourway.alert.streaming.settings.Settings;
import com.yourway.alert.utils.Util;
import com.yourway.alert.utils.UtilKafka;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.Optional;
import org.apache.spark.api.java.function.Function2;
import org.apache.spark.streaming.Durations;
import org.apache.spark.streaming.api.java.JavaDStream;
import org.apache.spark.streaming.api.java.JavaInputDStream;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import org.apache.spark.streaming.api.java.JavaStreamingContext;
import org.apache.spark.streaming.kafka010.ConsumerStrategies;
import org.apache.spark.streaming.kafka010.KafkaUtils;
import org.apache.spark.streaming.kafka010.LocationStrategies;
import scala.Tuple2;

import java.lang.reflect.Type;
import java.util.*;

public final class UserQuery {
    public static void main(String[] args) {
        Function2<List<JsonQuery>, Optional<JsonQuery>, Optional<JsonQuery>> updateFunction = (List<JsonQuery> maps, Optional<JsonQuery> hashMapOptional) -> {
            JsonQuery data;
            if (hashMapOptional.isPresent()) {
                data = hashMapOptional.get();
            } else {
                data = new JsonQuery();
            }

            // insert/update/delete query
            for (JsonQuery newQuery : maps) {
                HashMap<String, HashMap<String, Object>> query = newQuery.entrySet().iterator().next().getValue();
                String userId = newQuery.entrySet().iterator().next().getKey();
                String queryId = query.entrySet().iterator().next().getKey();
                HashMap<String, Object> infoQuery = query.entrySet().iterator().next().getValue();
                if (data.keySet().size() == 0) {
                    data.put(userId, new HashMap<>());
                }
                HashMap<String, Object> subQuery = query.get(queryId);
                if (subQuery.get("isDelete") == Boolean.TRUE) {
                    // delete
                    data.get(userId).remove(queryId);
                } else {
                    // update
                    data.get(userId).put(queryId, infoQuery);
                }
            }
            return Optional.of(data);
        };

        JsonQuery queries = Util.loadDataFromMySQL();

        ArrayList<JsonQuery> list = new ArrayList<>();
        queries.forEach((k, v) -> {
            JsonQuery a = new JsonQuery();
            a.put(k, v);
            list.add(a);
        });
        SparkConf conf = new SparkConf().setMaster("local[*]").setAppName("Storing User Query");
        JavaStreamingContext streamingContext = new JavaStreamingContext(conf, Durations.seconds(2));
        Queue<JavaRDD<JsonQuery>> rddQueue = new LinkedList<>();

        rddQueue.add(streamingContext.sparkContext().parallelize(list));

        JavaDStream<JsonQuery> dStream = streamingContext.queueStream(rddQueue);
        JavaPairDStream<String, JsonQuery> initialData = dStream.mapToPair(
                record -> new Tuple2<>(String.valueOf(record.entrySet().iterator().next().getKey()), record));
        try {
            streamingContext.sparkContext().setLogLevel("ERROR");
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
            Type type = new TypeToken<JsonQuery>() {
            }.getType();
            Properties props = UtilKafka.createProducer("KafkaProducer");
            JavaPairDStream<String, JsonQuery> results = inputKafka.mapToPair(
                    record -> new Tuple2<>(record.key(), (new Gson()).fromJson(record.value(), type))
            );
            results = results.union(initialData);
            results.print();
            JavaPairDStream<String, JsonQuery> newState = results.updateStateByKey(updateFunction);

            newState.print();

            UtilKafka.sendRDDToKafka(props, Settings.TOPIC_USER_QUERY, "userQuery", newState);

            streamingContext.start();
            streamingContext.awaitTermination();

            streamingContext.close();
            streamingContext.sparkContext().close();
            System.out.println("finish program!");
        } catch (IllegalStateException | NoSuchMethodError | InterruptedException e) {
            System.out.println(e.getMessage());
        } finally {
            streamingContext.close();
            streamingContext.sparkContext().close();
        }
    }
}
