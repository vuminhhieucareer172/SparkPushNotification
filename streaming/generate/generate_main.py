import argparse
from pathlib import Path

from streaming import settings
from streaming.generate.database import connect_database

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', type=str, default='example_gen_code.py', help='Path to file generated code')
parser.add_argument('-m', '--master', type=str, default='', help='IP master in spark cluster')
parser.add_argument('-n', '--app-name', type=str, default='Alert Job', help='Application name')
parser.add_argument('--level-log', type=str, default='ERROR', help='Enable log or not')
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
""".format("Job Alert Yourway", opt.level_log, settings.KAFKA_URI, settings.TOPIC_JOB)

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
""".format(table, 'select * from ' + table, table, settings.KAFKA_URI,
           settings.CHECKPOINT_PATH + '/query-' + str(record['id']),
           '1 second', settings.TOPIC_USER)

        r += """
    spark.streams.awaitAnyTermination()


if __name__ == '__main__':
    main()
"""
        f_gen.write(r)


if __name__ == '__main__':
    main()
