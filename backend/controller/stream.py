from datetime import datetime
from fastapi import status
from sqlalchemy import exc

from backend.controller.table import create_table_streaming
from backend.schemas.stream import Stream
from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from database import session

from apscheduler.schedulers.background import BackgroundScheduler
import requests
from starlette.responses import JSONResponse

from backend.models.job import Job
from constants import constants


def spark_version():
    version = requests.get(constants.SPARK_URL_API + '/version').json()
    return JSONResponse(version)


def get_list_applications():
    list_app = requests.get(constants.SPARK_URL_API + '/applications').json()
    return JSONResponse(list_app)


def get_detail_application(app_id: str):
    detail = requests.get(constants.SPARK_URL_API + '/applications/' + app_id).json()
    return JSONResponse(detail)


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
        return JSONResponse(content={"message": "Failed"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)
