from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
import requests
from backend.models.job import Job
from constants import constants


def spark_version():
    return requests.get(constants.SPARK_URL_API + '/version')


def get_list_applications():
    return requests.get(constants.SPARK_URL_API + '/applications')


def get_detail_application(app_id: str):
    return requests.get(constants.SPARK_URL_API + '/applications/' + app_id)


def get_list_job_stream():
    return 1
