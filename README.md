# YOURWAY WARNING JOB
# [![Flutter logo][]][flutter.dev]

Warning Job Yourway is a job alert system for users on [Yourway](https://yourway.vn)

## Prerequisites & Documentation

Make sure to install enough requirements before continue. All requirements are listed below:

* Operating systems: Linux, macOS
* Java version >= 11
* [Spark 3.x](https://spark.apache.org/downloads.html) & [docs](https://spark.apache.org/docs/latest/)
* [Kafka 2.x](https://kafka.apache.org/quickstart) & [docs](https://kafka.apache.org/documentation/)
* Maven


## Usage
### Start job user query

    spark-submit out/artifacts/userquery/yourway_warning_job.jar

### Start job warning job

    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 out/artifacts/userquery/yourway_warning_job.jar