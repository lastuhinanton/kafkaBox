package com.example.kafka;

import org.apache.kafka.clients.producer.*;
import org.apache.kafka.common.serialization.StringSerializer;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;

import java.util.Properties;
import java.util.UUID;

public class KafkaProducerApp {
    private static final Logger log = LogManager.getLogger(KafkaProducerApp.class);

    public static void main(String[] args) throws InterruptedException {
        String bootstrap = System.getenv().getOrDefault("BOOTSTRAP_SERVERS", "localhost:9092");
        String topic     = System.getenv().getOrDefault("TOPIC", "test-topic");
        int    interval  = Integer.parseInt(System.getenv().getOrDefault("INTERVAL_MS", "3000"));

        Properties props = new Properties();
        props.put(ProducerConfig.BOOTSTRAP_SERVERS_CONFIG, bootstrap);
        props.put(ProducerConfig.KEY_SERIALIZER_CLASS_CONFIG,   StringSerializer.class.getName());
        props.put(ProducerConfig.VALUE_SERIALIZER_CLASS_CONFIG, StringSerializer.class.getName());
        // (опционально) props.put(ProducerConfig.ACKS_CONFIG, "all");

        Producer<String, String> producer = new KafkaProducer<>(props);
        log.info("Starting producer to {} → {}", bootstrap, topic);

        int counter = 0;
        while (true) {
            String key   = "key-" + counter;
            String value = "value-" + UUID.randomUUID();
            ProducerRecord<String,String> rec = new ProducerRecord<>(topic, key, value);

            producer.send(rec, (metadata, ex) -> {
                if (ex == null) {
                    log.info("Sent {}→{} @{}:{} (offset {})",
                             rec.topic(), rec.value(),
                             metadata.partition(), metadata.timestamp(), metadata.offset());
                } else {
                    log.error("Send failed", ex);
                }
            });

            producer.flush();
            counter++;
            Thread.sleep(interval);
        }
    }
}