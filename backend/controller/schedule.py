import logging

import psutil
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from psutil import NoSuchProcess
from starlette import status
from starlette.responses import JSONResponse

from backend.utils.util_generate import generate_job_id
from backend.utils.util_get_config import get_config
from constants import constants
from constants.constants import GENERATE_STREAMING_SUCCESSFUL, CONFIG_JOB_STREAMING
from database.db import get_db, DB
from streaming.generate.generate_main import generate_job_stream
from streaming.spark import Spark

scheduler = BackgroundScheduler({
    'apscheduler.job_defaults.max_instances': '10'
})


def is_job_stream_running(pid):
    """ Check For the existence of a unix pid. """
    try:
        process = psutil.Process(pid)
        return "org.apache.spark.deploy.SparkSubmit" in process.cmdline()
    except NoSuchProcess:
        return False


def get_job_stream():
    spark_properties = get_config(constants.CONFIG_SPARK)
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
    return JSONResponse(content=dict(app_name=Spark().get_instanct().appName, schedule=schedule,
                                     is_running=is_job_stream_running(Spark().get_pid())),
                        status_code=status.HTTP_200_OK)


def job_exec(db: DB, job_id: str, job_name: str):
    result_generate = generate_job_stream(db, job_name, job_id)
    if result_generate != GENERATE_STREAMING_SUCCESSFUL:
        return result_generate
    process = Spark().submit_job_spark(job_id)
    logging.info(f"submitting job in process: {process.pid}")


def init_scheduler():
    db = get_db()
    if db is None:
        return "Fail to connect database"
    job_streaming_properties = get_config(CONFIG_JOB_STREAMING)
    if job_streaming_properties is None:
        return "missing job streaming config"

    job_streaming_properties = job_streaming_properties.value
    try:
        load_dotenv()
        job_name = job_streaming_properties.get("name_job", None)
        if job_name is None:
            return "missing config for name spark job"
        job_id = generate_job_id(job_name)

        schedule = job_streaming_properties.get("schedule", None)
        if schedule is None:
            return "missing schedule for spark job"

        job = scheduler.get_job(job_id=job_id)
        if job is not None:
            scheduler.remove_job(job_id=job_id)
        scheduler.add_job(job_exec, CronTrigger.from_crontab(schedule), id=job_id, args=[db, job_id, job_name])
        scheduler.start()
    except Exception as e:
        logging.error(e)
        return f"error {e}"
