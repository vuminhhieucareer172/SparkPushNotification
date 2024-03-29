from pydantic import BaseModel

from backend.schemas.table import Table


class Stream(BaseModel):
    table: Table
    topic_kafka_input: str


class JobStream(BaseModel):
    name_job: str
    schedule: str


class KafkaTopic(BaseModel):
    topic_name: str
