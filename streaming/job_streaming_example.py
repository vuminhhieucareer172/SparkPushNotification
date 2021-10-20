from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType

from constants.constants import KAFKA_URI, TOPIC_JOB, TOPIC_USER, CHECKPOINT_PATH


def main():
    concurrent_job = 3
    spark = SparkSession \
        .builder \
        .appName("Job Alert Yourway") \
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.sparkContext.setLogLevel("ERROR")
    spark.conf.set("spark.streaming.concurrentJobs", str(concurrent_job))

    df = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_URI) \
        .option("subscribe", TOPIC_JOB) \
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

    data_job.createOrReplaceTempView("userId")
    data = spark.sql("select * from userId where salary > 1.0")
    check_matching = udf(
        lambda x: "userId--5--" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))

    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_URI) \
        .option("checkpointLocation", CHECKPOINT_PATH + '/user1') \
        .trigger(processingTime='5 minutes') \
        .option("topic", TOPIC_USER).start()

    data_job.createOrReplaceTempView("job")
    data = spark.sql("select * from job where salary > 1.0")
    check_matching = udf(
        lambda x: "job--10--" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", KAFKA_URI) \
        .option("checkpointLocation", CHECKPOINT_PATH + '/user2') \
        .trigger(continuous='10 minutes') \
        .option("topic", TOPIC_USER).start()

    spark.streams.awaitAnyTermination()


if __name__ == '__main__':
    main()
