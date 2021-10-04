import csv
import json
import random

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, expr, json_tuple, from_json, col
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType, Row

from settings import KAFKA_URI, DICT_MAX_AGE, DICT_MIN_AGE, \
    TOPIC_JOB, TOPIC_USER_QUERY, FIELD_JOB, FIELD_QUERY

decode_string = udf(lambda x: x.decode('utf-8'), StringType())


def matching(queries, address: str, age=None, salary=None, year=None, edu_level=None, job_attribute=None):
    user_id = []
    if age is not None:
        array_age = age.split(',')
        if len(array_age) > 1:
            min_age = int(DICT_MIN_AGE[array_age[0]])
            max_age = int(DICT_MAX_AGE[array_age[-1]])
        else:
            min_age = 0
            max_age = 200
    else:
        min_age = 0
        max_age = 200

    # for query in queries:
    #     # is_number_salary = True
    #     # if salary is not None:
    #     #     is_number_salary = query['salary'] >= float(salary)
    #     #
    #     # is_not_none_address = False
    #     # if address is not None:
    #     #     is_not_none_address = query['company_address'] in address
    #     # try:
    #     #     # if is_not_none_address and min_age <= int(query[2]) <= max_age and is_number_salary and \
    #     #     #         query[4] == year and query[5] == edu_level and query[6] == job_attribute:
    #     #     if min_age <= int(query['age']) <= max_age and is_number_salary:
    #     #         user_id.append(
    #     #             dict(user_id=query['user_id'], contact=query['contact'])
    #     #         )
    #     # except Exception as e:
    #     #     logging.error(e)
    #     for i in range(1000):
    #         a = 1 + 1
    #     user_id.append(
    #         dict(user_id=query['user_id'], contact=query['contact'])
    #     )

    # return '[' + ','.join(str(x) for x in user_id) + ']'
    return str(random.randint(1, 100000))


def read_data():
    data = []
    with open('user_query.csv', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            data.append(row)
    return json.loads(json.dumps(data, indent=4))


def main():
    spark = SparkSession \
        .builder \
        .appName("Job Alert Yourway") \
        .getOrCreate()
    spark.sparkContext.setLogLevel("ERROR")
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.crossJoin.enabled", "true")
    df_job = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_URI) \
        .option("subscribe", TOPIC_JOB) \
        .load()
    df_query = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_URI) \
        .option("subscribe", TOPIC_USER_QUERY) \
        .load()
    schema_job = StructType([
        StructField("id", LongType()),
        StructField("application_deadline", DateType()),
        StructField("company_address", IntegerType()),
        StructField("salary", FloatType()),
        StructField("ages", StringType()),
        StructField("education_level", StringType()),
        StructField("position", StringType()),
        StructField("job_attribute", StringType()),
        StructField("year_experiences", FloatType()),
    ])
    schema_query = StructType([
        StructField("query_id", LongType()),
        StructField("query_user_id", LongType()),
        StructField("query_company_address", StringType()),
        StructField("query_job_role", StringType()),
        StructField("query_age", IntegerType()),
        StructField("query_salary", FloatType()),
        StructField("query_year_experiences", FloatType()),
        StructField("query_education_level", StringType()),
        StructField("query_job_attribute", StringType()),
        StructField("query_contact", StringType()),
        StructField("query_group_by", StringType()),
        StructField("query_slide_window", StringType()),
    ])

    data_job = df_job.withColumn(
        "data", from_json(col("value").astype(StringType()), schema_job)
    ).select("key", "offset", "partition", "timestamp", "timestampType", "topic", "data.*")

    data_query = df_query.withColumn(
        "data", from_json(col("value").astype(StringType()), schema_query)
    ).select("key", "offset", "partition", "timestamp", "timestampType", "topic", "data.*")

    data = data_job.alias("JOB").join(data_query.alias("QUERY"), expr("""
        QUERY.query_job_attribute = JOB.job_attribute AND
        QUERY.query_job_role = JOB.position AND
        JOB.education_level = QUERY.query_education_level AND
        JOB.company_address like concat("%", QUERY.query_company_address, "%") AND
        JOB.salary >= QUERY.query_salary AND
        QUERY.timestamp <= JOB.timestamp + interval 1 hour AND
        QUERY.timestamp > JOB.timestamp
    """), "full_outer")

    # check_matching = udf(
    #     lambda address, age, salary, year, edu_level, job_attribute:
    #     matching(address, age, salary, year, edu_level, job_attribute), StringType()
    # )
    #
    # # match
    # data = data.withColumn(
    #     "value", check_matching(data["company_address"], data["ages"], data["salary"], data["year_experiences"],
    #                             data["education_level"], data["job_attribute"])
    # )
    #
    # data = data.withColumn(
    #     "key", col("id")
    # )
    #
    # data = data.filter(col("value").isNotNull())

    # run app
    # app = data \
    #     .writeStream \
    #     .format("kafka") \
    #     .option("kafka.bootstrap.servers", KAFKA_URI) \
    #     .option("checkpointLocation", CHECKPOINT_PATH) \
    #     .option("topic", TOPIC_USER) \
    #     .start()
    app = data \
        .writeStream \
        .format('console') \
        .start()

    app.awaitTermination()


if __name__ == '__main__':
    main()
