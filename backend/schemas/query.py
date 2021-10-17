from pydantic import BaseModel


class Query(BaseModel):
    sql: str
    topic_kafka_output: str
    time_trigger: str
    contact: dict


class QueryUpdate(BaseModel):
    id: int
    sql: str
    topic_kafka_output: str
    time_trigger: str
    contact: dict
