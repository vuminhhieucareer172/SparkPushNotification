# YOURWAY WARNING JOB
<img width="500" alt="warning yourway" src="https://scontent.fhan3-4.fna.fbcdn.net/v/t1.6435-9/230843670_2992572540998317_4807766980010250166_n.jpg?_nc_cat=106&_nc_rgb565=1&ccb=1-5&_nc_sid=09cbfe&_nc_ohc=gfU521T_9aUAX_b2v18&_nc_ht=scontent.fhan3-4.fna&oh=62749455f98be9fcb9705e02e266812a&oe=61457618">


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
