import json
import time

from confluent_kafka import Producer

from database.db import get_db
from database.session import SchemaEncoder

conf = {
    'bootstrap.servers': 'localhost:9092',
    'message.max.bytes': 1000000000,
    'queue.buffering.max.kbytes': 2147483647,
    'queue.buffering.max.messages': 10000000
}


def send_message_to_kafka(table_fake_data: str, topic: str, limit: int = 10):
    producer = Producer(conf)
    db = get_db()
    result = db.engine.execute("select * from {} limit {}".format(table_fake_data, limit))
    count = 1
    data = list(map(lambda record: json.loads(json.dumps(dict(record), cls=SchemaEncoder, ensure_ascii=False)), result))
    for row in data:
        message = json.dumps(row, ensure_ascii=False)
        producer.produce(topic=topic, key='aaa', value=message)
        print(f"sending data to {topic}, #{count}: {message}")
        count += 1
        producer.flush()


if __name__ == '__main__':
    send_message_to_kafka(topic='dbstreaming_streaming_mobile', table_fake_data='dbstreaming_streaming_mobile')
