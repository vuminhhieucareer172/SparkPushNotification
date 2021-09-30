#!/bin/bash

echo "Start program"

spark-submit --packages mysql:mysql-connector-java:5.1.49  out/artifacts/userquery/yourway_job_alert.jar

echo "Finish program!"
