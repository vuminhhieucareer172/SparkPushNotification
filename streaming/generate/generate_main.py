import argparse

from constants import constants
from database import db
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, default='streaming/job_stream/job/', help='Path to file generated code')
parser.add_argument('-ep', '--exec-path', type=str, default='streaming/job_stream/executor/',
                    help='Path to file generated code')
parser.add_argument('-m', '--master', type=str, default='spark://192.168.1.5:7077', help='IP master in spark cluster')
parser.add_argument('-n', '--app-name', type=str, default='Alert Job', help='Application name')
parser.add_argument('--level-log', type=str, default='ERROR', help='Enable log or not')
parser.add_argument('--network-timeout', type=str, default='fourier', help='Model to predict')
parser.add_argument('--executor-instances', type=str, default='fourier', help='Model to predict')
parser.add_argument('--cores-max', type=int, default=6, help='Model to predict')
parser.add_argument('--executor-memory', type=str, default='1g', help='Size executor memory')
opt = parser.parse_args()


def get_query():
    return db.execute("select * from query")


def main():
    file_name = opt.app_name.lower().replace(" ", "_") + ".py"
    data = get_query()
    with open(opt.path + file_name, 'w') as f_job:
        r = """from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType

def main():
    concurrent_job = 3
    spark = SparkSession \\
        .builder \\
        .appName("{}") \\
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.sparkContext.setLogLevel("{}")
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
    ).select("key", "offset", "partition", "timestamp", "timestampType", "topic", "data.*")
""".format("Job Alert Yourway", opt.level_log, constants.KAFKA_URI, constants.TOPIC_JOB)

        for record in data:
            table = 'table' + str(record['id'])
            r += """
    data_job.createOrReplaceTempView("{}")
    data = spark.sql("{}")
    check_matching = udf(
        lambda x: "{}----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \\
        .format("kafka") \\
        .option("kafka.bootstrap.servers", "{}") \\
        .option("checkpointLocation", "{}") \\
        .trigger(processingTime='{}') \\
        .option("topic", "{}").start()
""".format(table, 'select * from ' + table, table, constants.KAFKA_URI,
           constants.CHECKPOINT_PATH + '/query-' + str(record['id']),
           '1 second', constants.TOPIC_USER)

        r += """
    spark.streams.awaitAnyTermination()


if __name__ == '__main__':
    main()
"""
        f_job.write(r)

    with open(opt.exec_path + file_name, 'w') as f_exec:
        f_exec.write("""import os

def run():
    os.system("spark-submit --master {} --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 {}")
        """.format(opt.master, opt.path + file_name))


if __name__ == '__main__':
    main()
