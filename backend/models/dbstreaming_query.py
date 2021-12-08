from sqlalchemy import Column, VARCHAR, INTEGER, JSON, TIMESTAMP, func, TEXT
from sqlalchemy.ext.declarative import declarative_base

Model = declarative_base()


class UserQuery(Model):
    __tablename__ = "dbstreaming_query"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    sql = Column(TEXT(), nullable=False)
    topic_kafka_output = Column(VARCHAR(50), nullable=False)
    time_trigger = Column(VARCHAR(50), nullable=False, default='60')
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), server_onupdate=func.now())
    contact = Column(JSON, nullable=True)

    def __init__(self, **kwargs):
        super(UserQuery, self).__init__(**kwargs)
