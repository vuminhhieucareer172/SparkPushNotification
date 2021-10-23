import json

from confluent_kafka import Consumer, Producer
from constants.constants import KAFKA_URI, TOPIC_JOB
from kafka import KafkaProducer

producer = Producer({'bootstrap.servers': '10.0.2.5:9092'})

mess = {
        "date": "20/09/2032 01:55:19",
        "skill_experience": 1251,
        "benefit": 2.54646,
        "salary": 21474834800,
        "name": "Viện Nghiên cứu Dữ liệu lớn - VinBigdata",
        }

# mess = {"type": str(type("dgasdg"))}
a = json.dumps(mess)
producer.produce(TOPIC_JOB, a)
producer.flush()
