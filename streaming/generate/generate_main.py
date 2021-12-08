import sqlalchemy.engine
from sqlalchemy import inspect

from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from backend.models.dbstreaming_query import UserQuery
from backend.utils.util_get_config import get_config
from constants import constants
from constants.constants import PREFIX_DB_TABLE_STREAMING, GENERATE_STREAMING_SUCCESSFUL
from database.db import DB, get_session, get_db
from database.session import SessionHandler
from streaming.generate.generate_database_schema import get_schema_table, get_list_column_of_table
import sqlparse

from streaming.generate.generate_sql_statements import format_sql_spark


def build_import():
    return """from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf, to_json, struct
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType,\\
DatetimeConverter, TimestampType, ArrayType, ShortType, BinaryType, DecimalType, DoubleType, MapType"""


def build_setup(app_name: str, **kwargs):
    return """
def main():
    concurrent_job = 3
    spark = SparkSession \\
        .builder \\
        .appName("{}") \\
        .getOrCreate()
    conf = spark.sparkContext.getConf().setAll(
        [('spark.executor.memory', '4g'), ('spark.app.name', '{}'), ('spark.executor.cores', '4'),
         ('spark.cores.max', '12'), ('spark.driver.memory', '4g')])
    spark.sparkContext.stop()
    spark = SparkSession.builder.config(conf=conf).getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.conf.set("spark.sql.streaming.stateStore.stateSchemaCheck", "false")
    spark.sparkContext.setLogLevel("{}")
    spark.conf.set("spark.streaming.concurrentJobs", str(concurrent_job))""".format(app_name, app_name,
                                                                                    kwargs.get("log_level", "ERROR"))


def build_schema_and_input(content: str, bootstrap_servers: str, db: DB, inspector: sqlalchemy.engine.Inspector):
    tables = inspector.get_table_names()
    query_session = SessionHandler.create(get_session(database=db), KafkaStreaming)
    for table in tables:
        if table.startswith(PREFIX_DB_TABLE_STREAMING):
            mapping_kafka_streaming = query_session.get_one(query_dict=dict(table_streaming=table))
            if mapping_kafka_streaming is None:
                raise ValueError(f"table {table} has not corresponding topic kafka")
            content += """
    {} = spark \\
        .readStream \\
        .format("kafka") \\
        .option("kafka.bootstrap.servers", "{}") \\
        .option("subscribe", "{}") \\
        .load()""".format(table, bootstrap_servers, mapping_kafka_streaming.topic_kafka)
            content += """
    schema_{} = {}
    """.format(table, get_schema_table(inspector, table))

            content += """
    data_{} = {}.withColumn(
        "data", from_json(col("value").astype(StringType()), schema_{})
    ).select("data.*")
    """.format(table, table, table)

            content += """
    data_{}.createOrReplaceTempView("{}")
    """.format(table, table)
    return content


def build_sql_and_output(content: str, bootstrap_servers: str, data: list, inspector: sqlalchemy.engine.Inspector):
    for record in data:
        sql: str = record['sql']
        parsed = sqlparse.parse(sql)
        if len(sqlparse.split(sql)) > 1:
            print("unsupported more than 1 sql statements, use only first statement!")
            sql = sqlparse.split(sql)[0]
        if parsed[0].get_type() != "SELECT":
            raise ValueError("only supported sql statements type SELECT")

        sql = format_sql_spark(sql=sql, inspector=inspector)

        content += """
    data = spark.sql("{}")
    function_key = udf(lambda x: "{}", StringType())
    data = data.withColumn("value", to_json(struct([c for c in data.columns])))
    data = data.withColumn("key", function_key(col("value")))
    data.writeStream \\
        .format("kafka") \\
        .option("kafka.bootstrap.servers", "{}") \\
        .option("checkpointLocation", "{}") \\
        .option("topic", "{}"){}.start()
    """.format(sql, 'query-' + str(record['id']), bootstrap_servers, constants.CHECKPOINT_PATH + '/query-' + str(record['id']), record['topic_kafka_output'],
               '.outputMode("complete")' if 'group by' in sql.lower() else '')
    return content


def build_ending():
    return """
    spark.streams.awaitAnyTermination()


if __name__ == '__main__':
    main()
"""


def generate_job_stream(db: DB, app_name: str, file_job_name: str, path_job_folder: str = 'streaming/job_stream/job/',
                        **kwargs):
    session = get_session(database=db)
    try:
        query_session = SessionHandler.create(session, UserQuery)
        data = query_session.get_all(to_json=True)

        if data is None:
            return "No query in database"
        spark_config = get_config(constants.CONFIG_SPARK)
        if spark_config is None:
            return "No config spark in database"
        kafka_config = get_config(constants.CONFIG_KAFKA)
        if kafka_config is None:
            return "No config kafka in database"

        with open(path_job_folder + file_job_name + ".py", 'w') as f_job:
            # import dependency
            r = build_import()

            # init spark app with name and log level
            r += build_setup(app_name=app_name, **kwargs)

            # set other config
            for config in kwargs.keys():
                r += """
    spark.conf.set("{}", "{}")""".format(config, kwargs.get(config))

            # read from streaming tables in db
            inspector = inspect(db.engine)
            r = build_schema_and_input(r, kafka_config.value['bootstrap.servers'], db, inspector)

            # generate query
            r = build_sql_and_output(r, kafka_config.value['bootstrap.servers'], data, inspector)

            r += build_ending()

            f_job.write(r)
            f_job.close()
        return GENERATE_STREAMING_SUCCESSFUL
    except Exception as e:
        print(e)
        return "Error {}".format(str(e))


if __name__ == '__main__':
    print(generate_job_stream(get_db(), app_name="dbstreaming", file_job_name="dbstreaming"))
