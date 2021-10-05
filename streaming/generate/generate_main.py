import argparse
from pathlib import Path

import settings
from generate.database import connect_database

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, default='example_gen_code.py', help='Path to file generated code')
parser.add_argument('--master', type=str, default='datasets/NN5_FINAL_DATASET_WITH_TEST_DATA.xls',
                    help='IP master in spark cluster')
parser.add_argument('--app-name', type=str, default='fourier', help='Application name')
parser.add_argument('--enable-log', type=bool, default=False, help='Enable log or not')
parser.add_argument('--network-timeout', type=str, default='fourier', help='Model to predict')
parser.add_argument('--executor-instances', type=str, default='fourier', help='Model to predict')
parser.add_argument('--cores-max', type=int, default=6, help='Model to predict')
parser.add_argument('--executor-memory', type=str, default='1g', help='Size executor memory')
opt = parser.parse_args()


def get_query():
    db = connect_database()
    return db.execute("select * from query")


def main():
    Path(opt.path).touch()
    data = get_query()
    with open(opt.path, 'w') as f_gen:
        r = """from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType

def init_app():
    spark = SparkSession \\
        .builder \\
        .appName("Job Alert Yourway") \\
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.sparkContext.setLogLevel("ERROR")
    return spark

def main():
    concurrent_job = 3
    spark = SparkSession \\
        .builder \\
        .appName("{}") \\
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.sparkContext.setLogLevel("ERROR")
    spark.conf.set("spark.streaming.concurrentJobs", str(concurrent_job))

    df = spark \\
        .readStream \\
        .format("kafka") \\
        .option("kafka.bootstrap.servers", "{}") \\
        .option("subscribe", "{}") \\
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
    data_job = df.withColumn(
        "data", from_json(col("value").astype(StringType()), schema_job)
    ).select("key", "offset", "partition", "timestamp", "timestampType", "topic", "data.*") \\
        .withColumn("value", col("key"))
""".format("Job Alert Yourway", settings.KAFKA_URI, settings.TOPIC_JOB, )
        count = 0
        for record in data:
            if count < 100:
                count += 1
            else:
                break
            table = 'table' + str(record['user_id'])
            r += """
    data_job.createOrReplaceTempView("{}")
    data = spark.sql("{}")
    data.writeStream \\
        .format("kafka") \\
        .option("kafka.bootstrap.servers", "{}") \\
        .option("checkpointLocation", "{}") \\
        .trigger(processingTime='{}') \\
        .option("topic", "{}").start()
""".format(table, 'select * from ' + table, settings.KAFKA_URI, settings.CHECKPOINT_PATH + '/user-' + str(record['user_id']),
           '1 second', settings.TOPIC_USER)

        r += """
    spark.streams.awaitAnyTermination()
"""
        f_gen.write(r)


if __name__ == '__main__':
    main()
