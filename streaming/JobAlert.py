import json
import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, json_tuple, col
from pyspark.sql.types import StringType

from settings import TOPIC_USER, FIELD_JOB, KAFKA_URI, CHECKPOINT_PATH, DICT_MAX_AGE, DICT_MIN_AGE, \
    TOPIC_JOB, TOPIC_USER_QUERY
from utils.util_kafka import get_latest_message

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
    for query in queries:
        # is_number_salary = True
        # if salary is not None:
        #     is_number_salary = query['salary'] >= float(salary)
        #
        # is_not_none_address = False
        # if address is not None:
        #     is_not_none_address = query['company_address'] in address
        # try:
        #     # if is_not_none_address and min_age <= int(query[2]) <= max_age and is_number_salary and \
        #     #         query[4] == year and query[5] == edu_level and query[6] == job_attribute:
        #     if min_age <= int(query['age']) <= max_age and is_number_salary:
        #         user_id.append(
        #             dict(user_id=query['user_id'], contact=query['contact'])
        #         )
        # except Exception as e:
        #     logging.error(e)
        # time.sleep(0.01)
        user_id.append(
            dict(user_id=query['user_id'], contact=query['contact'])
        )

    return '[' + ','.join(str(x) for x in user_id) + ']'


def main():
    spark = SparkSession \
        .builder \
        .appName("Job Alert Yourway") \
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_URI) \
        .option("subscribe", TOPIC_JOB) \
        .load()
    spark.sparkContext.setLogLevel("ERROR")

    data = df.select(
        json_tuple(
            decode_string(df["value"]),
            *FIELD_JOB
        ).alias(*FIELD_JOB)
    )
    user_queries = get_latest_message(topic=TOPIC_USER_QUERY, group_id="KafkaProducer")
    data_json = json.loads(user_queries)
    print(len(data_json))

    check_matching = udf(
        lambda address, age, salary, year, edu_level, job_attribute:
        matching(data_json, address, age, salary, year, edu_level, job_attribute), StringType()
    )

    # match
    start = time.time()
    data = data.withColumn(
        "value", check_matching(data["company_address"], data["ages"], data["salary"], data["year_experiences"],
                                data["education_level"], data["job_attribute"])
    )
    print(time.time() - start)

    data = data.withColumn(
        "key", col("id")
    )

    data = data.filter(col("value").isNotNull())

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
