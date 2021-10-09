from datetime import datetime

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
