package utils;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import settings.Settings;

import java.io.Serializable;
import java.util.Properties;

public class KafkaSink<K, V> implements Serializable {
    private final Producer<K, V> producer;

    public KafkaSink() {
        this.producer = createProducer();
    }

    private Producer<K, V> createProducer() {
        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, Settings.KAFKA_URI);
        props.put(ProducerConfig.CLIENT_ID_CONFIG, "KafkaProducer");
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        return new KafkaProducer<>(props);
    }

    public void send(String topic, K key, V value) throws Exception {
        long time = System.currentTimeMillis();
        try {
                final ProducerRecord<K, V> record = new ProducerRecord<>(topic, key, value);

                RecordMetadata metadata = producer.send(record).get();

                long elapsedTime = System.currentTimeMillis() - time;
                System.out.printf("sent record(key=%s value=%s) meta(partition=%d, offset=%d) time=%d\n",
                        record.key(), record.value(), metadata.partition(), metadata.offset(), elapsedTime);
        } finally {
            this.producer.flush();
            this.producer.close();
        }
    }

    public void closeProducer() {
        this.producer.flush();
        this.producer.close();
    }
}
