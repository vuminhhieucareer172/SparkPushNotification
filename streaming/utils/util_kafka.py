from confluent_kafka import Consumer

from constants.constants import KAFKA_URI, TOPIC_JOB
import json

settings = {
    "bootstrap.servers": KAFKA_URI,
    "group.id": 'group_id',
    "enable.auto.commit": True,
    "session.timeout.ms": 6000,
    "default.topic.config": {"auto.offset.reset": "earliest"},
}
consumer = Consumer(settings)
def get_latest_message(topic: str, group_id: str = '') -> str:
    global consumer, settings
    def on_assign(a_consumer, partitions):
        last_offset = a_consumer.get_watermark_offsets(partitions[0])
        partitions[0].offset = last_offset[1] - 1
        consumer.assign(partitions)

    consumer.subscribe([topic], on_assign=on_assign)

    msg = consumer.poll(5.0)
    print('msg', msg.value())
    return msg.value().decode('utf-8')


if __name__ == '__main__':
    data = get_latest_message(TOPIC_JOB, '')
    data_json = json.loads(data)
    print(data)
