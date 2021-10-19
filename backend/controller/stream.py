from apscheduler.triggers.cron import CronTrigger
from fastapi import status
from fastapi.responses import RedirectResponse
from sqlalchemy import exc
from starlette.responses import JSONResponse
import subprocess

from backend.controller.schedule import generate_job_id, scheduler
from backend.controller.table import create_table_streaming
from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from backend.schemas.stream import Stream
from backend.utils.util_get_config import get_config_spark
from database import session
from streaming.spark import spark, spark_sql


def check_status_spark():
    spark_config = get_config_spark()
    if spark_config is None:
        return JSONResponse(content={"message": "Error database"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        print(spark_config.value.get("master") + ":8888")
        return RedirectResponse("http://" + spark_config.value.get("master") + ":8888")
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Failed", "detail": e}, status_code=status.HTTP_400_BAD_REQUEST)


def add_stream(new_schema: Stream):
    is_create_table_success = create_table_streaming(new_schema.table)
    if is_create_table_success.status_code != status.HTTP_201_CREATED:
        return is_create_table_success

    try:
        session.add(KafkaStreaming.from_json(new_schema.table.name, new_schema.topic_kafka_input))
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": e}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def submit_job_spark(file: str):
    cmd = "nohup", "spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2", \
          "streaming/job_stream/job/" + file + ".py"
    proc = subprocess.Popen(cmd)
    return proc


def get_job_stream():
    spark_properties = get_config_spark()
    if spark_properties is None:
        return None
    spark_properties = spark_properties.value
    if spark_properties.get("name_job", None) is None:
        return JSONResponse(content={"message": "missing config for name spark job"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    job = scheduler.get_job(job_id=generate_job_id(
        spark_properties.get("name_job"))
    )

    schedule = {}
    for field in CronTrigger.FIELD_NAMES:
        field_name = CronTrigger.FIELD_NAMES.index(field)
        schedule[field] = str(job.trigger.fields[field_name])
    return JSONResponse(content=dict(app_name=spark.appName, schedule=schedule),
                        status_code=status.HTTP_200_OK)


def stop_job_streaming():
    spark_sql.stop()
    return JSONResponse(content={"message": "stopped"}, status_code=status.HTTP_200_OK)


def start_job_streaming():
    job = submit_job_spark(file="job_streaming_example")
    return JSONResponse(content={"message": "started", "process_id": job.pid}, status_code=status.HTTP_200_OK)
