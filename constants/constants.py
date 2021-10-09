KAFKA_URI = "localhost:9092"
TOPIC_JOB = "jobYourway"
TOPIC_USER = "userId"
TOPIC_USER_QUERY = "userQuery"

SQLALCHEMY_ENGINE_OPTIONS = {
    "max_overflow": 30,
    "pool_size": 100
}

CHECKPOINT_PATH = "checkpoint"

PREFIX_DB_TABLE_STREAMING = "dbstreaming_streaming_"
PREFIX_DB_TABLE_QUERY = "dbstreaming_query_"
