import sqlalchemy

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

DATA_TYPE_SQLALCHEMY = {
    "VARCHAR": sqlalchemy.VARCHAR,
    "INTEGER": sqlalchemy.INTEGER,
    "TEXT": sqlalchemy.TEXT,
    "DATETIME": sqlalchemy.DATETIME,
    "TIMESTAMP": sqlalchemy.TIMESTAMP,
    "DATE": sqlalchemy.DATE,
    "FLOAT": sqlalchemy.FLOAT,
    "ARRAY": sqlalchemy.ARRAY,
    "CHAR": sqlalchemy.CHAR,
    "BIGINT": sqlalchemy.BIGINT,
    "TIME": sqlalchemy.TIME,
    "SMALLINT": sqlalchemy.SMALLINT,
    "BINARY": sqlalchemy.BINARY,
    "VARBINARY": sqlalchemy.VARBINARY,
    "DECIMAL": sqlalchemy.DECIMAL,
    "BLOB": sqlalchemy.BLOB,
    "CLOB": sqlalchemy.CLOB,
    "REAL": sqlalchemy.REAL,
    "JSON": sqlalchemy.JSON,
    "ENUM": sqlalchemy.Enum,
    "UNICODE": sqlalchemy.Unicode,
}

DATATYPE_STRING = [sqlalchemy.VARCHAR, sqlalchemy.TEXT, sqlalchemy.CHAR, sqlalchemy.BINARY, sqlalchemy.VARBINARY,
                   sqlalchemy.BLOB, sqlalchemy.CLOB, sqlalchemy.Unicode]
DATATYPE_NUMERIC = [sqlalchemy.INTEGER, sqlalchemy.BIGINT, sqlalchemy.SMALLINT, sqlalchemy.BOOLEAN, sqlalchemy.FLOAT,
                    sqlalchemy.DECIMAL, sqlalchemy.REAL]
DATATYPE_DATE_AND_TIME = [sqlalchemy.DATETIME, sqlalchemy.TIMESTAMP, sqlalchemy.DATE, sqlalchemy.TIME]
DATATYPE_SPECIAL = [sqlalchemy.ARRAY, sqlalchemy.Enum, sqlalchemy.JSON]
