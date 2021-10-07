KAFKA_URI = 'localhost:9092'
TOPIC_JOB = 'jobYourway'
TOPIC_USER = 'userId'
TOPIC_USER_QUERY = 'userQuery'

DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = "yourway"
DB_USERNAME = "yourway"
DB_PASSWORD = "Jobalert@123"
DB_CHARSET = 'utf8mb4'

SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + str(DB_PORT) + '/' + \
                          DB_NAME + '?charset=' + DB_CHARSET

SQLALCHEMY_ENGINE_OPTIONS = {
    'max_overflow': 30,
    'pool_size': 100
}

CHECKPOINT_PATH = 'checkpoint'
