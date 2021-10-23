from sqlalchemy import Column, VARCHAR, INTEGER, JSON, TIMESTAMP, func
from database.db import Model
from backend.schemas.query import Query


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
    def from_json(schema_query: Query):
        return UserQuery(
            sql=schema_query.sql,
            topic_kafka_output=schema_query.topic_kafka_output,
            time_trigger=schema_query.time_trigger,
            contact=schema_query.contact,
        )
