from sqlalchemy import Column, VARCHAR, INTEGER, JSON, TIMESTAMP, func

from database import Model


class UserQuery(Model):
    __tablename__ = "dbstreaming_query"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    sql = Column(VARCHAR(50), nullable=False)
    topic_kafka_output = Column(VARCHAR(50), nullable=False)
    time_trigger = Column(VARCHAR(50), nullable=False, default='1 second')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())
    contact = Column(JSON, nullable=True)

    def __init__(self, **kwargs):
        super(UserQuery, self).__init__(**kwargs)

    def to_full_json(self):
        return dict(
            id=self.id,
            sql=self.sql,
            topic_kafka_output=self.topic_kafka_output,
            time_trigger=self.time_trigger,
            created_at=self.created_at,
            updated_at=self.updated_at,
            contact=self.contact,
        )

    @staticmethod
    def from_json(json_post):
        return UserQuery(
            sql=json_post.get('sql'),
            topic_kafka_output=json_post.get('topic_kafka_output'),
            time_trigger=json_post.get('time_trigger'),
            contact=json_post.get('contact'),
        )
