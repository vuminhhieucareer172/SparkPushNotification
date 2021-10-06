from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, udf
from pyspark.sql.types import StringType, StructType, IntegerType, StructField, DateType, LongType, FloatType

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
    ).select("key", "offset", "partition", "timestamp", "timestampType", "topic", "data.*")

    data_job.createOrReplaceTempView("table1")
    data = spark.sql("select * from table1")
    check_matching = udf(
        lambda x: "table1----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-1") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table2")
    data = spark.sql("select * from table2")
    check_matching = udf(
        lambda x: "table2----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-2") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table3")
    data = spark.sql("select * from table3")
    check_matching = udf(
        lambda x: "table3----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-3") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table4")
    data = spark.sql("select * from table4")
    check_matching = udf(
        lambda x: "table4----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-4") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table5")
    data = spark.sql("select * from table5")
    check_matching = udf(
        lambda x: "table5----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-5") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table6")
    data = spark.sql("select * from table6")
    check_matching = udf(
        lambda x: "table6----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-6") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table7")
    data = spark.sql("select * from table7")
    check_matching = udf(
        lambda x: "table7----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-7") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table8")
    data = spark.sql("select * from table8")
    check_matching = udf(
        lambda x: "table8----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-8") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table9")
    data = spark.sql("select * from table9")
    check_matching = udf(
        lambda x: "table9----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-9") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table10")
    data = spark.sql("select * from table10")
    check_matching = udf(
        lambda x: "table10----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-10") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table11")
    data = spark.sql("select * from table11")
    check_matching = udf(
        lambda x: "table11----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-11") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table12")
    data = spark.sql("select * from table12")
    check_matching = udf(
        lambda x: "table12----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-12") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table13")
    data = spark.sql("select * from table13")
    check_matching = udf(
        lambda x: "table13----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-13") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table14")
    data = spark.sql("select * from table14")
    check_matching = udf(
        lambda x: "table14----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-14") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table15")
    data = spark.sql("select * from table15")
    check_matching = udf(
        lambda x: "table15----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-15") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table16")
    data = spark.sql("select * from table16")
    check_matching = udf(
        lambda x: "table16----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-16") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table17")
    data = spark.sql("select * from table17")
    check_matching = udf(
        lambda x: "table17----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-17") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table18")
    data = spark.sql("select * from table18")
    check_matching = udf(
        lambda x: "table18----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-18") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table19")
    data = spark.sql("select * from table19")
    check_matching = udf(
        lambda x: "table19----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-19") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table20")
    data = spark.sql("select * from table20")
    check_matching = udf(
        lambda x: "table20----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-20") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table21")
    data = spark.sql("select * from table21")
    check_matching = udf(
        lambda x: "table21----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-21") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table22")
    data = spark.sql("select * from table22")
    check_matching = udf(
        lambda x: "table22----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-22") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table23")
    data = spark.sql("select * from table23")
    check_matching = udf(
        lambda x: "table23----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-23") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table24")
    data = spark.sql("select * from table24")
    check_matching = udf(
        lambda x: "table24----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-24") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table25")
    data = spark.sql("select * from table25")
    check_matching = udf(
        lambda x: "table25----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-25") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table26")
    data = spark.sql("select * from table26")
    check_matching = udf(
        lambda x: "table26----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-26") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table27")
    data = spark.sql("select * from table27")
    check_matching = udf(
        lambda x: "table27----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-27") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table28")
    data = spark.sql("select * from table28")
    check_matching = udf(
        lambda x: "table28----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-28") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table29")
    data = spark.sql("select * from table29")
    check_matching = udf(
        lambda x: "table29----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-29") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table30")
    data = spark.sql("select * from table30")
    check_matching = udf(
        lambda x: "table30----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-30") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table31")
    data = spark.sql("select * from table31")
    check_matching = udf(
        lambda x: "table31----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-31") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table32")
    data = spark.sql("select * from table32")
    check_matching = udf(
        lambda x: "table32----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-32") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table33")
    data = spark.sql("select * from table33")
    check_matching = udf(
        lambda x: "table33----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-33") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table34")
    data = spark.sql("select * from table34")
    check_matching = udf(
        lambda x: "table34----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-34") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table35")
    data = spark.sql("select * from table35")
    check_matching = udf(
        lambda x: "table35----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-35") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table36")
    data = spark.sql("select * from table36")
    check_matching = udf(
        lambda x: "table36----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-36") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table37")
    data = spark.sql("select * from table37")
    check_matching = udf(
        lambda x: "table37----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-37") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table38")
    data = spark.sql("select * from table38")
    check_matching = udf(
        lambda x: "table38----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-38") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table39")
    data = spark.sql("select * from table39")
    check_matching = udf(
        lambda x: "table39----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-39") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table40")
    data = spark.sql("select * from table40")
    check_matching = udf(
        lambda x: "table40----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-40") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table41")
    data = spark.sql("select * from table41")
    check_matching = udf(
        lambda x: "table41----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-41") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table42")
    data = spark.sql("select * from table42")
    check_matching = udf(
        lambda x: "table42----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-42") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table43")
    data = spark.sql("select * from table43")
    check_matching = udf(
        lambda x: "table43----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-43") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table44")
    data = spark.sql("select * from table44")
    check_matching = udf(
        lambda x: "table44----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-44") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table45")
    data = spark.sql("select * from table45")
    check_matching = udf(
        lambda x: "table45----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-45") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table46")
    data = spark.sql("select * from table46")
    check_matching = udf(
        lambda x: "table46----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-46") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table47")
    data = spark.sql("select * from table47")
    check_matching = udf(
        lambda x: "table47----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-47") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table48")
    data = spark.sql("select * from table48")
    check_matching = udf(
        lambda x: "table48----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-48") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table49")
    data = spark.sql("select * from table49")
    check_matching = udf(
        lambda x: "table49----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-49") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table50")
    data = spark.sql("select * from table50")
    check_matching = udf(
        lambda x: "table50----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-50") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table51")
    data = spark.sql("select * from table51")
    check_matching = udf(
        lambda x: "table51----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-51") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table52")
    data = spark.sql("select * from table52")
    check_matching = udf(
        lambda x: "table52----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-52") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table53")
    data = spark.sql("select * from table53")
    check_matching = udf(
        lambda x: "table53----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-53") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table54")
    data = spark.sql("select * from table54")
    check_matching = udf(
        lambda x: "table54----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-54") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table55")
    data = spark.sql("select * from table55")
    check_matching = udf(
        lambda x: "table55----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-55") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table56")
    data = spark.sql("select * from table56")
    check_matching = udf(
        lambda x: "table56----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-56") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table57")
    data = spark.sql("select * from table57")
    check_matching = udf(
        lambda x: "table57----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-57") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table58")
    data = spark.sql("select * from table58")
    check_matching = udf(
        lambda x: "table58----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-58") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table59")
    data = spark.sql("select * from table59")
    check_matching = udf(
        lambda x: "table59----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-59") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table60")
    data = spark.sql("select * from table60")
    check_matching = udf(
        lambda x: "table60----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-60") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table61")
    data = spark.sql("select * from table61")
    check_matching = udf(
        lambda x: "table61----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-61") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table62")
    data = spark.sql("select * from table62")
    check_matching = udf(
        lambda x: "table62----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-62") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table63")
    data = spark.sql("select * from table63")
    check_matching = udf(
        lambda x: "table63----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-63") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table64")
    data = spark.sql("select * from table64")
    check_matching = udf(
        lambda x: "table64----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-64") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table65")
    data = spark.sql("select * from table65")
    check_matching = udf(
        lambda x: "table65----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-65") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table66")
    data = spark.sql("select * from table66")
    check_matching = udf(
        lambda x: "table66----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-66") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table67")
    data = spark.sql("select * from table67")
    check_matching = udf(
        lambda x: "table67----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-67") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table68")
    data = spark.sql("select * from table68")
    check_matching = udf(
        lambda x: "table68----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-68") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table69")
    data = spark.sql("select * from table69")
    check_matching = udf(
        lambda x: "table69----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-69") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table70")
    data = spark.sql("select * from table70")
    check_matching = udf(
        lambda x: "table70----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-70") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table71")
    data = spark.sql("select * from table71")
    check_matching = udf(
        lambda x: "table71----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-71") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table72")
    data = spark.sql("select * from table72")
    check_matching = udf(
        lambda x: "table72----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-72") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table73")
    data = spark.sql("select * from table73")
    check_matching = udf(
        lambda x: "table73----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-73") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table74")
    data = spark.sql("select * from table74")
    check_matching = udf(
        lambda x: "table74----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-74") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table75")
    data = spark.sql("select * from table75")
    check_matching = udf(
        lambda x: "table75----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-75") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table76")
    data = spark.sql("select * from table76")
    check_matching = udf(
        lambda x: "table76----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-76") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table77")
    data = spark.sql("select * from table77")
    check_matching = udf(
        lambda x: "table77----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-77") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table78")
    data = spark.sql("select * from table78")
    check_matching = udf(
        lambda x: "table78----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-78") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table79")
    data = spark.sql("select * from table79")
    check_matching = udf(
        lambda x: "table79----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-79") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table80")
    data = spark.sql("select * from table80")
    check_matching = udf(
        lambda x: "table80----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-80") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table81")
    data = spark.sql("select * from table81")
    check_matching = udf(
        lambda x: "table81----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-81") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table82")
    data = spark.sql("select * from table82")
    check_matching = udf(
        lambda x: "table82----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-82") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table83")
    data = spark.sql("select * from table83")
    check_matching = udf(
        lambda x: "table83----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-83") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table84")
    data = spark.sql("select * from table84")
    check_matching = udf(
        lambda x: "table84----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-84") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table85")
    data = spark.sql("select * from table85")
    check_matching = udf(
        lambda x: "table85----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-85") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table86")
    data = spark.sql("select * from table86")
    check_matching = udf(
        lambda x: "table86----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-86") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table87")
    data = spark.sql("select * from table87")
    check_matching = udf(
        lambda x: "table87----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-87") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table88")
    data = spark.sql("select * from table88")
    check_matching = udf(
        lambda x: "table88----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-88") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table89")
    data = spark.sql("select * from table89")
    check_matching = udf(
        lambda x: "table89----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-89") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table90")
    data = spark.sql("select * from table90")
    check_matching = udf(
        lambda x: "table90----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-90") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table91")
    data = spark.sql("select * from table91")
    check_matching = udf(
        lambda x: "table91----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-91") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table92")
    data = spark.sql("select * from table92")
    check_matching = udf(
        lambda x: "table92----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-92") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table93")
    data = spark.sql("select * from table93")
    check_matching = udf(
        lambda x: "table93----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-93") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table94")
    data = spark.sql("select * from table94")
    check_matching = udf(
        lambda x: "table94----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-94") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table95")
    data = spark.sql("select * from table95")
    check_matching = udf(
        lambda x: "table95----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-95") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table96")
    data = spark.sql("select * from table96")
    check_matching = udf(
        lambda x: "table96----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-96") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table97")
    data = spark.sql("select * from table97")
    check_matching = udf(
        lambda x: "table97----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-97") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table98")
    data = spark.sql("select * from table98")
    check_matching = udf(
        lambda x: "table98----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-98") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table99")
    data = spark.sql("select * from table99")
    check_matching = udf(
        lambda x: "table99----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-99") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    data_job.createOrReplaceTempView("table100")
    data = spark.sql("select * from table100")
    check_matching = udf(
        lambda x: "table100----" + str(x), StringType()
    )
    data = data.withColumn("value", check_matching(col("key")))
    data.writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("checkpointLocation", "checkpoint/query-100") \
        .trigger(processingTime='1 second') \
        .option("topic", "userId").start()

    spark.streams.awaitAnyTermination()


if __name__ == '__main__':
    main()
