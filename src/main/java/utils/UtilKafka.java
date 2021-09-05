package utils;

import com.google.common.collect.Maps;
import com.google.gson.Gson;
import models.JsonQuery;
import org.apache.kafka.clients.consumer.ConsumerConfig;
import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringDeserializer;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.spark.streaming.api.java.JavaPairDStream;
import settings.Settings;

import java.time.Duration;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;

public class UtilKafka {

    public static Properties createProducer(String groupId) {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, Settings.KAFKA_URI);
        props.put(ProducerConfig.CLIENT_ID_CONFIG, groupId);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        return props;
    }

    public static Properties createConsumer(String groupId) {
        Properties props = new Properties();
        props.put(ConsumerConfig.BOOTSTRAP_SERVERS_CONFIG, Settings.KAFKA_URI);
        props.put(ConsumerConfig.GROUP_ID_CONFIG, groupId);
        props.put(ConsumerConfig.KEY_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        props.put(ConsumerConfig.VALUE_DESERIALIZER_CLASS_CONFIG, StringDeserializer.class.getName());
        return props;
    }

    public static void sendRDDToKafka(Properties props, String topic, String key, JavaPairDStream<String, JsonQuery> rdd) {
        rdd.foreachRDD(eRdd -> {
            Gson gson = new Gson();
            long time = System.currentTimeMillis();
            Producer<String, String> producer = new KafkaProducer<>(props);
            try {
                List<JsonQuery> list = eRdd.values().collect();
                HashMap<String, Object> map = new HashMap<>();
                for (JsonQuery e : list)
                    map.put(e.entrySet().iterator().next().getKey(), e.entrySet().iterator().next().getValue());

                if (!list.isEmpty()) {
                    final ProducerRecord<String, String> record = new ProducerRecord<>(
                            topic, key, gson.toJson(map)
                    );
                    RecordMetadata metadata = producer.send(record).get();
                    long elapsedTime = System.currentTimeMillis() - time;
                    System.out.printf("sent record(key=%s value=%s) meta(partition=%d, offset=%d) time=%d\n",
                            record.key(), record.value(), metadata.partition(), metadata.offset(), elapsedTime);
                }
            } finally {
                producer.flush();
                producer.close();
            }
        });
    }

    public static void sendMessageToKafka(Properties props, String topic, String key, String message) throws Exception {
        long time = System.currentTimeMillis();
        Producer<String, String> producer = new KafkaProducer<>(props);
        try {
            final ProducerRecord<String, String> record = new ProducerRecord<>(
                    topic, key, message
            );
            RecordMetadata metadata = producer.send(record).get();
            long elapsedTime = System.currentTimeMillis() - time;
            System.out.printf("sent record(key=%s value=%s) meta(partition=%d, offset=%d) time=%d\n",
                    record.key(), record.value(), metadata.partition(), metadata.offset(), elapsedTime);
        } finally {
            producer.flush();
            producer.close();
        }
    }

    public static ConsumerRecord<String, String> getLatestMessage(Properties propsKafka, String topic) {
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(propsKafka);
        consumer.subscribe(Collections.singletonList(topic));

        consumer.poll(Duration.ofSeconds(10));

        consumer.assignment().forEach(System.out::println);

        AtomicLong maxTimestamp = new AtomicLong();
        AtomicReference<ConsumerRecord<String, String>> latestRecord = new AtomicReference<>();

        // get the last offsets for each partition
        consumer.endOffsets(consumer.assignment()).forEach((topicPartition, offset) -> {
            // seek to the last offset of each partition
            consumer.seek(topicPartition, (offset == 0) ? offset : offset - 1);

            // poll to get the last record in each partition
            consumer.poll(Duration.ofSeconds(10)).forEach(record -> {

                // the latest record in the 'topic' is the one with the highest timestamp
                if (record.timestamp() > maxTimestamp.get()) {
                    maxTimestamp.set(record.timestamp());
                    latestRecord.set(record);
                }
            });
        });
        consumer.close();
        return latestRecord.get();
    }
}
