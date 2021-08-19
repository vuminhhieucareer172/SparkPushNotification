package utils;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.apache.kafka.clients.consumer.KafkaConsumer;
import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import settings.Settings;

import java.time.Duration;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Properties;
import java.util.concurrent.atomic.AtomicLong;
import java.util.concurrent.atomic.AtomicReference;

public class UtilKafka {

    private Producer createProducer() {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, Settings.KAFKA_URI);
        props.put(ProducerConfig.CLIENT_ID_CONFIG, "KafkaProducer");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        return new KafkaProducer<>(props);
    }

//    public void send(String topic, K key, V value) throws Exception {
//        long time = System.currentTimeMillis();
//        try {
//            final ProducerRecord<K, V> record = new ProducerRecord<>(topic, key, value);
//
//            RecordMetadata metadata = producer.send(record).get();
//
//            long elapsedTime = System.currentTimeMillis() - time;
//            System.out.printf("sent record(key=%s value=%s) meta(partition=%d, offset=%d) time=%d\n",
//                    record.key(), record.value(), metadata.partition(), metadata.offset(), elapsedTime);
//        } finally {
//            this.producer.flush();
//            this.producer.close();
//        }
//    }
//
//    public void closeProducer() {
//        this.producer.flush();
//        this.producer.close();
//    }

    public static ConsumerRecord<String, String> getLatestMessage(Properties propsKafka, String topic) {
        KafkaConsumer<String, String> consumer = new KafkaConsumer<>(propsKafka);
        consumer.subscribe(Collections.singletonList(topic));

        consumer.poll(Duration.ofSeconds(10));

        consumer.assignment().forEach(System.out::println);

        AtomicLong maxTimestamp = new AtomicLong();
        AtomicReference<ConsumerRecord<String, String>> latestRecord = new AtomicReference<>();

        // get the last offsets for each partition
        consumer.endOffsets(consumer.assignment()).forEach((topicPartition, offset) -> {
            System.out.println("offset: " + offset);

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
        System.out.println(latestRecord.get());
        return latestRecord.get();
    }
}
