import subprocess

from fastapi import status
from fastapi.responses import RedirectResponse
from sqlalchemy import exc
from starlette.responses import JSONResponse

from backend.controller.table import create_table_streaming
from backend.models.dbstreaming_config import Config
from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from backend.schemas.configuration import Configuration
from backend.schemas.stream import Stream, JobStream
from backend.utils.util_get_config import get_config
from constants import constants
from database import session
from streaming.spark import spark_sql


def check_status_spark():
    spark_config = get_config(constants.CONFIG_SPARK)
    if spark_config is None:
        return JSONResponse(content={"message": "Error database"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        return RedirectResponse("http://" + spark_config.value.get("master") + ":8888")
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Failed", "detail": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)


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
        return JSONResponse(content={"message": "Failed", "detail": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def submit_job_spark(file: str):
    cmd = "nohup", "spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2", \
          "streaming/job_stream/job/" + file + ".py"
    proc = subprocess.Popen(cmd)
    return proc


def stop_job_streaming():
    spark_sql.stop()
    return JSONResponse(content={"message": "stopped"}, status_code=status.HTTP_200_OK)


def start_job_streaming():
    job = submit_job_spark(file="job_streaming_example")
    return JSONResponse(content={"message": "started", "process_id": job.pid}, status_code=status.HTTP_200_OK)


def update_job_streaming(schema: JobStream):
    try:
        job_streaming = session.query(Config).filter(Config.id == constants.CONFIG_JOB_STREAMING).scalar()
        if job_streaming is not None:
            job_streaming.value = dict(name_job=schema.name_job,
                                       schedule=schema.schedule)
        else:
            config_schema = Configuration(name=constants.CONFIG_JOB_STREAMING,
                                          value=dict(name_job=schema.name_job,
                                                     schedule=schema.schedule)
                                          )
            session.add(Config.from_json(config_schema))
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)
