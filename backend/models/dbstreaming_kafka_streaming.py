from sqlalchemy import Column, VARCHAR, INTEGER

from database import Model


class KafkaStreaming(Model):
    __tablename__ = "dbstreaming_kafka_streaming"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    topic_kafka = Column(VARCHAR(50), nullable=False)
    table_streaming = Column(VARCHAR(50), nullable=False)

    def __init__(self, **kwargs):
        super(KafkaStreaming, self).__init__(**kwargs)

    def to_full_json(self):
        return dict(
            id=self.id,
            table_streaming=self.table_streaming,
            topic_kafka=self.topic_kafka,
        )

    @staticmethod
    def from_json(json_post):
        return KafkaStreaming(
            table_streaming=json_post.get('table_streaming'),
            topic_kafka=json_post.get('topic_kafka'),
        )
