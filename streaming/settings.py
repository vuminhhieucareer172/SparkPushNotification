KAFKA_URI = 'localhost:9092'
TOPIC_JOB = 'jobYourway'
TOPIC_USER = 'userId'
TOPIC_SET_USER_QUERY = 'setUserQuery'
TOPIC_USER_QUERY = 'userQuery'

FIELD_JOB = ["id", "application_deadline", "company_address", "company_name", "job_benefits", "job_descriptions",
             "job_formality", "job_other_info", "job_requirements", "job_trial_period", "salary", "skills", "title",
             "url", "ages", "education_level", "genders", "domains", "position", "job_attribute", "locations", "time",
             "year_experiences", "position_number"]

FIELD_QUERY = ['query_id', 'query_user_id', 'query_name', 'query_type_query', 'query_company_address',
               'query_job_role', 'query_age', 'query_salary', 'query_year_experiences', 'query_education_level',
               'query_job_attribute', 'query_contact', 'query_group_by', 'query_slide_window']

CHECKPOINT_PATH = 'checkpoint'
DICT_MIN_AGE = {
    'Dưới 18': 0,
    '18-30': 18,
    '30-40': 30,
    '40-50': 40,
    '50-60': 50,
    'Trên 60': 60
}
DICT_MAX_AGE = {
    'Dưới 18': 18,
    '18-30': 30,
    '30-40': 40,
    '40-50': 50,
    '50-60': 60,
    'Trên 60': 200
}

DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = "yourway"
DB_USERNAME = "yourway"
DB_PASSWORD = "Jobalert@123"
DB_CHARSET = 'utf8mb4'

SQLALCHEMY_DATABASE_URI = 'mysql://' + DB_USERNAME + ':' + DB_PASSWORD + '@' + DB_HOST + ':' + str(DB_PORT) + '/' + \
                          DB_NAME + '?charset=' + DB_CHARSET
