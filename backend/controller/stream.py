import json

from apscheduler.triggers.cron import CronTrigger
from fastapi import status
from fastapi.responses import RedirectResponse
from sqlalchemy import exc, Table, MetaData, text, inspect
from sqlalchemy.engine import Inspector
from starlette.responses import JSONResponse

from backend.controller.schedule import scheduler
from backend.controller import table
from backend.models.dbstreaming_config import Config
from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from backend.schemas.configuration import Configuration
from backend.schemas.stream import Stream, JobStream
from backend.utils.util_get_config import get_config
from constants import constants
from constants.constants import ID_JOB_STREAM, PREFIX_DB_TABLE_STREAMING
from database.db import DB, get_session
from database.session import SessionHandler, SchemaEncoder
from streaming.spark import Spark


def check_status_spark(db: DB):
    spark_config = get_config(constants.CONFIG_SPARK)
    if spark_config is None:
        return JSONResponse(content={"message": "Error database"}, status_code=status.HTTP_400_BAD_REQUEST)
    try:
        return RedirectResponse("http://" + spark_config.value.get("master") + ":4040")
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def get_all_stream(db: DB):
    session = get_session(database=db)
    try:
        stream_session = SessionHandler.create(session, KafkaStreaming)
        list_topic_stream = []
        list_stream = []
        inspector: Inspector = inspect(db.engine)
        list_table = inspector.get_table_names()
        for table_name in list_table:
            if table_name.startswith(PREFIX_DB_TABLE_STREAMING):
                list_stream.append(table_name)
        for stream in list_stream:
            object_stream_kafka = stream_session.get_one(query_dict=dict(table_streaming=stream))
            if object_stream_kafka is None:
                stream_object = {
                    'table': stream,
                    'topic_kafka': ''
                }
            else:
                stream_object = {
                    'table': stream,
                    'topic_kafka': object_stream_kafka.topic_kafka
                }
            list_topic_stream.append(stream_object)
    except exc.SQLAlchemyError as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(list_topic_stream, status_code=status.HTTP_200_OK)


def get_stream_by_name(stream_name: str, db: DB):
    session = get_session(database=db)
    json_result = {}
    try:
        if not stream_name.startswith(PREFIX_DB_TABLE_STREAMING):
            return JSONResponse(content={"message": "Invalid stream name"}, status_code=status.HTTP_400_BAD_REQUEST)
        stream_session = SessionHandler.create(session, KafkaStreaming)
        stream_update = stream_session.get_one(query_dict=dict(table_streaming=stream_name))
        if stream_update is None:
            return JSONResponse(content={"message": "Not found stream {}".format(stream_name)},
                                status_code=status.HTTP_404_NOT_FOUND)
        json_result['topic_kafka_input'] = stream_update.topic_kafka
        json_result['table'] = table.get_info_table(stream_name, db)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(json_result, status_code=status.HTTP_200_OK)


def get_record_by_stream_name(table_stream: str, db: DB, skip: int = 0, limit: int = 10):
    session = get_session(database=db)
    try:
        if not table_stream.startswith(PREFIX_DB_TABLE_STREAMING):
            return JSONResponse(content={"message": "Invalid stream name"}, status_code=status.HTTP_404_NOT_FOUND)
        query = Table(table_stream, MetaData(db.engine), autoload=True)
        record_session = SessionHandler.create(session, query)
        records = record_session.get_from_offset(skip=skip, limit=limit)
        data = list(map(
            lambda record: json.loads(json.dumps(dict(record), cls=SchemaEncoder, ensure_ascii=False)), records))
        return JSONResponse(data, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def add_stream(new_schema: Stream, db: DB):
    session = get_session(database=db)
    is_create_table_success = table.create_table(new_schema.table, db)
    if is_create_table_success.status_code != status.HTTP_201_CREATED:
        return is_create_table_success
    try:
        stream_session = SessionHandler.create(session, KafkaStreaming)
        stream_session.add(dict(table_streaming=new_schema.table.name, topic_kafka=new_schema.topic_kafka_input))
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def update_stream(new_schema: Stream, db: DB):
    session = get_session(database=db)
    try:
        stream_session = SessionHandler.create(session, KafkaStreaming)
        stream_update = stream_session.get_one(query_dict=dict(table_streaming=new_schema.table.name))
        if stream_update is None:
            return JSONResponse(content={"message": "Not found stream {}".format(new_schema.table.name)},
                                status_code=status.HTTP_404_NOT_FOUND)
        is_update_table_success = table.update_table(new_schema.table, db)
        if is_update_table_success.status_code != status.HTTP_200_OK:
            return is_update_table_success
        stream_update.topic_kafka = new_schema.topic_kafka_input
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)


def delete_stream(stream_name: str, db: DB):
    session = get_session(database=db)
    try:
        stream_session = SessionHandler.create(session, KafkaStreaming)

        # delete constraint kafka topic with table
        stream_session.delete(query_dict=dict(table_streaming=stream_name))

        # drop table corresponding to stream
        meta = MetaData(db.engine)
        table_stream = Table(stream_name, meta, autoload=True)
        table_stream.drop()

        session.commit()
    except exc.NoSuchTableError as e:
        print(e)
        return JSONResponse(content={"message": "Not found table {}".format(stream_name)},
                            status_code=status.HTTP_404_NOT_FOUND)
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)


def stop_job_streaming():
    try:
        Spark().get_sql_context().sparkSession.stop()
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"message": "stopped"}, status_code=status.HTTP_200_OK)


def start_job_streaming():
    try:
        process_id = Spark().submit_job_spark(file="job_streaming_example")
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"message": "started", "process_id": process_id}, status_code=status.HTTP_200_OK)


def update_job_streaming(schema: JobStream, db: DB):
    session = get_session(database=db)
    try:
        job_streaming_session = SessionHandler.create(session, Config)
        job_streaming = job_streaming_session.get_one(query_dict=dict(id=constants.CONFIG_JOB_STREAMING))
        if job_streaming is not None:
            job_streaming.value = dict(name_job=schema.name_job, schedule=schema.schedule)
        else:
            config_schema = Configuration(name=constants.CONFIG_JOB_STREAMING,
                                          value=dict(name_job=schema.name_job,
                                                     schedule=schema.schedule)
                                          )
            job_streaming_session.add(config_schema.dict())
        scheduler.modify_job(job_id=ID_JOB_STREAM, trigger=CronTrigger.from_crontab(schema.schedule))
        if not scheduler.running:
            scheduler.start()
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)
