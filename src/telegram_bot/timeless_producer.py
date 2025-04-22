from confluent_kafka import Producer
import sys, random, time

# kafka configuration
kafka_config = {
  'bootstrap.servers': 'node1:9092,node2:9092,node3:9092',
  'client.id': 'timeless-producer',
  'acks': 'all'
}

producer = Producer(kafka_config)

def delivery_report(err, msg):
  """Callback function to confirm message delivery"""
  if err is not None:
    print(f"Message delivery failed: {err}")
  else:
    print(f"Message delivered to {msg.topic()} [partition: {msg.partition()} offset: {msg.offset()}]")


def produce_messages():
  while True:
    key_number = random.uniform(1.0, 21.0)
    try:
      producer.produce("TIMELESS_PRODUCER", key=str(key_number), value=f"Message with key {key_number}")
    except Exception as e:
      print(f"Error producing message: {e}")
    producer.flush()
    time.sleep(int(1))

if __name__ == "__main__":
  produce_messages()
