import os

def run():
    os.system("spark-submit --master spark://192.168.1.5:7077 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2 streaming/job_stream/job/alert_job.py")
        