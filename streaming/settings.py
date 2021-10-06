KAFKA_URI = 'localhost:9092'
TOPIC_JOB = 'jobYourway'
TOPIC_USER = 'userId'
TOPIC_USER_QUERY = 'userQuery'

CHECKPOINT_PATH = 'checkpoint'

DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = "yourway"
DB_USERNAME = "yourway"
DB_PASSWORD = "Jobalert@123"
DB_CHARSET = 'utf8mb4'

SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + str(DB_PORT) + '/' + \
                          DB_NAME + '?charset=' + DB_CHARSET
