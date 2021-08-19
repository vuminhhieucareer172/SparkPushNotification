# YOURWAY WARNING JOB


## run job user query

    spark-submit out/artifacts/userquery/yourway_warning_job.jar

## run job warning job

    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 out/artifacts/userquery/yourway_warning_job.jar