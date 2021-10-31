from fastapi import status
from fastapi.responses import RedirectResponse
from sqlalchemy import exc, Table
from starlette.responses import JSONResponse

from backend.controller.table import create_table, update_table
from backend.models.dbstreaming_config import Config
from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from backend.schemas.configuration import Configuration
from backend.schemas.stream import Stream, JobStream
from backend.utils.util_get_config import get_config
from constants import constants
from constants.constants import PREFIX_DB_TABLE_STREAMING
from database.db import session, meta
from streaming.spark import Spark


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
    is_create_table_success = create_table(new_schema.table)
    if is_create_table_success.status_code != status.HTTP_201_CREATED:
        return is_create_table_success
    try:
        session.add(KafkaStreaming.from_json(PREFIX_DB_TABLE_STREAMING + new_schema.table.name,
                                             new_schema.topic_kafka_input))
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def update_stream(new_schema: Stream):
    try:
        stream_update: KafkaStreaming = session.query(KafkaStreaming).filter_by(table_streaming=new_schema.table.name)\
            .first()
        if stream_update is None:
            return JSONResponse(content={"message": "Not found stream {}".format(new_schema.table.name)},
                                status_code=status.HTTP_400_BAD_REQUEST)

        is_update_table_success = update_table(new_schema.table)

        if is_update_table_success.status_code != status.HTTP_200_OK:
            return is_update_table_success
        stream_update.topic_kafka = new_schema.topic_kafka_input
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)


def delete_stream(stream_name: str):
    try:
        # delete constraint kafka topic with table
        stream_delete: KafkaStreaming = session.query(KafkaStreaming).filter_by(table_streaming=stream_name).first()
        session.delete(stream_delete)

        # drop table corresponding to stream
        table_stream = Table(stream_name, meta, autoload=True)
        table_stream.drop()

        session.commit()
    except exc.NoSuchTableError as e:
        return JSONResponse(content={"message": "Not found table {}".format(stream_name)}, status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)


def stop_job_streaming():
    Spark().get_sql_context().stop()
    return JSONResponse(content={"message": "stopped"}, status_code=status.HTTP_200_OK)


def start_job_streaming():
    job = Spark().submit_job_spark(file="job_streaming_example")
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
