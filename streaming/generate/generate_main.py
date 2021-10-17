from sqlalchemy import inspect

from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from backend.utils.util_get_config import get_config_spark, get_config_kafka
from constants import constants
from constants.constants import PREFIX_DB_TABLE_STREAMING
from database import db, session, engine
from streaming.generate.generate_database_schema import get_schema_table


def get_query():
    return db.execute("select * from dbstreaming_query")


def generate_job_stream(app_name: str, file_job_name: str, path_job_folder: str = 'streaming/job_stream/job/',
                        path_executor_folder: str = 'streaming/job_stream/executor/', **kwargs):
    data = get_query()
    spark_config = get_config_spark().value
    kafka_config = get_config_kafka().value

    with open(path_job_folder + file_job_name, 'w') as f_job:
        # import dependency
        r = """from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType,
DatetimeConverter, TimestampType, ArrayType, ShortType, BinaryType, DecimalType, DoubleType, MapType"""

        # init spark app with name and log level
        r += """
def main():
    concurrent_job = 3
    spark = SparkSession \\
        .builder \\
        .appName("{}") \\
        .getOrCreate()
    conf = spark.sparkContext.getConf().setAll(
        [('spark.executor.memory', '4g'), ('spark.app.name', 'Job Alert Yourway'), ('spark.executor.cores', '4'),
         ('spark.cores.max', '12'), ('spark.driver.memory', '4g')])
    spark.sparkContext.stop()
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.sparkContext.setLogLevel("{}")
    spark.conf.set("spark.streaming.concurrentJobs", str(concurrent_job))""".format(app_name,
                                                                                    kwargs.get("log_level", "ERROR"))

        # set other config
        for config in kwargs.keys():
            r += """
    spark.conf.set("{}", "{}")""".format(config, kwargs.get(config))

        # read from streaming tables in db
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        for table in tables:
            if table.startswith(PREFIX_DB_TABLE_STREAMING):
                mapping_kafka_streaming = session.query(KafkaStreaming).filter_by(table_streaming=table).scalar()
                r += """
    {} = spark \\
        .readStream \\
        .format("kafka") \\
        .option("kafka.bootstrap.servers", "{}") \\
        .option("subscribe", "{}") \\
        .load()""".format(table, kafka_config['bootstrap.servers'], mapping_kafka_streaming.topic_kafka)
                r += """
    schema_{} = {}
""".format(table, get_schema_table(inspector, table))

                r += """
    data_{} = df.withColumn(
        "data", from_json(col("value").astype(StringType()), schema_{})
    ).select("key", "offset", "partition", "timestamp", "timestampType", "topic", "data.*")
""".format(table, table)

                r += """
    data_{}.createOrReplaceTempView("{}")
""".format(table, table)

        # generate query
        for record in data:
            table_name = 'table' + str(record['id'])
            r += """
    data = spark.sql("{}")
    check_matching = udf(
        lambda x: "{}----" + str({}), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \\
        .format("kafka") \\
        .option("kafka.bootstrap.servers", "{}") \\
        .option("checkpointLocation", "{}") \\
        .trigger(processingTime='{}') \\
        .option("topic", "{}").start()
""".format(record['sql'], table_name, record['id'], kafka_config['bootstrap.servers'],
           constants.CHECKPOINT_PATH + '/query-' + str(record['id']), record['time_trigger'], record['topic_kafka_output'])

        r += """
    spark.streams.awaitAnyTermination()

if __name__ == '__main__':
    main()
"""
        f_job.write(r)

    with open(path_executor_folder + file_job_name, 'w') as f_exec:
        f_exec.write("""import os
def run():
    os.system("spark-submit --master {} --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 {}")
        """.format(spark_config['master'], path_job_folder + file_job_name))
