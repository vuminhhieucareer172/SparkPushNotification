from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType

def init_app():
    spark = SparkSession \
        .builder \
        .appName("Job Alert Yourway") \
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.sparkContext.setLogLevel("ERROR")
    return spark

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
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "jobYourway") \
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
    ).select("key", "offset", "partition", "timestamp", "timestampType", "topic", "data.*") \
        .withColumn("value", col("key"))

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/user-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    spark.streams.awaitAnyTermination()
