# YOURWAY WARNING JOB
<img width="800" alt="warning yourway" src="https://user-images.githubusercontent.com/50447619/130323874-63729001-4f17-4c72-afb5-22542de9c861.png">

Warning Job Yourway is a job alert system for users on [Yourway](https://yourway.vn)

## Prerequisites & Documentation

Make sure to install enough requirements before continue. All requirements are listed below:

* Operating systems: Linux, macOS
* Java version >= 11
* [Spark 3.x](https://spark.apache.org/downloads.html) & [docs](https://spark.apache.org/docs/latest/)
* [Kafka 2.x](https://kafka.apache.org/quickstart) & [docs](https://kafka.apache.org/documentation/)
* Maven

Config kafka information in class Settings then run the following command to build file jar:

    mvn install

## Usage
### Start job user query

    spark-submit out/artifacts/userquery/yourway_warning_job.jar

### Start job warning job

    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 out/artifacts/userquery/yourway_warning_job.jar
