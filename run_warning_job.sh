#!/bin/bash

echo "Start program"

spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 out/artifacts/userquery/yourway_job_alert.jar

echo "Finish program!"
