import json
from json import JSONDecodeError

from confluent_kafka import Consumer

from backend.utils.util_get_config import get_config


class Kafka:
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """

        if Kafka.__instance is not None:
            raise Exception(
                "This class is a singleton, use Kafka.create()")
        else:
            Kafka.__instance = self
        self.consumer = self.create_consumer()

    @staticmethod
    def create():
        if Kafka.__instance is None:
            Kafka.__instance = Kafka()
        return Kafka.__instance

    @staticmethod
    def get_credentials():
        """ Fetch credentials from either environment variables (for testing)"""
        kafka_config = get_config('kafka')
        if kafka_config is None or kafka_config.value.get('bootstrap.servers', None) is None:
            return None
        return {
            "bootstrap.servers": kafka_config.value['bootstrap.servers'],
            "group.id": 'group_id',
            "enable.auto.commit": True,
            "session.timeout.ms": 6000,
            "default.topic.config": {"auto.offset.reset": "earliest"},
        }

    def create_consumer(self):
        return Consumer(self.get_credentials())


def get_list_topics():
    kafka = Kafka.create()
    if kafka.consumer is None:
        return 'Fail to connect kafka'
    if not kafka.consumer.list_topics().topics:
        return 'Not found any topic'
    dict_key = kafka.consumer.list_topics().topics.keys()
    list_topic = []
    for topic in dict_key:
        list_topic.append(topic)
    return list_topic


def get_latest_message(topic: str):
    try:
        kafka = Kafka.create()
        if topic not in kafka.consumer.list_topics().topics.keys():
            return {}, 'Not found topic {} in kafka server'.format(topic)

        def on_assign(a_consumer, partitions):
            last_offset = a_consumer.get_watermark_offsets(partitions[0])
            partitions[0].offset = last_offset[1] - 1
            kafka.consumer.assign(partitions)

        kafka.consumer.subscribe([topic], on_assign=on_assign)

        msg = kafka.consumer.poll(5.0)
        if msg is None:
            return {}, 'Topic {} does not have any message!'.format(topic)

        message_value = msg.value().decode('utf-8')
        try:
            return json.loads(message_value), ''
        except JSONDecodeError as e:
            print(e)
            return {}, 'Cannot decode string {} to json'.format(message_value)
    except TypeError as e:
        print(e)
        return {}, 'TypeError: {}'.format(str(e))
    except Exception as e:
        print(e)
        return {}, 'error: {}'.format(str(e))


if __name__ == '__main__':
    # data = get_latest_message(TOPIC_JOB, '')
    get_list_topics()
    # data_json = json.loads(data)
    # print(data)
