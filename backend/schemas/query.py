from pydantic import BaseModel


class Query(BaseModel):
    sql: str
    topic_kafka_output: str
    time_trigger: str
    contact: dict
