from sqlalchemy import Column, VARCHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class KafkaStreaming(Model):
    __tablename__ = "dbstreaming_kafka_streaming"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    topic_kafka = Column(VARCHAR(50), nullable=False)
    table_streaming = Column(VARCHAR(50), nullable=False, unique=True)

    def __init__(self, **kwargs):
        super(KafkaStreaming, self).__init__(**kwargs)
