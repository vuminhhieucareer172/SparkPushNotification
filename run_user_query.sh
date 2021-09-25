#!/bin/bash

echo "Start program"

spark-submit --packages mysql:mysql-connector-java:5.1.49  out/artifacts/userquery/yourway_warning_job.jar

echo "Finish program!"
