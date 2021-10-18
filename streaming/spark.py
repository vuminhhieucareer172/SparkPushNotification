from pyspark.sql import SparkSession


def init_app():
    spark = SparkSession \
        .builder \
        .appName("Job Alert Yourway") \
        .getOrCreate()
    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", "true")
    spark.conf.set("spark.sql.legacy.timeParserPolicy", "LEGACY")
    spark.sparkContext.setLogLevel("ERROR")
    return spark


spark_instance = init_app()
spark_pid = None
