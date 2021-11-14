import logging

import apscheduler.job
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from starlette import status
from starlette.responses import JSONResponse

from backend.utils.util_get_config import get_config
from backend.utils.util_process import is_process_running
from constants import constants
from constants.constants import GENERATE_STREAMING_SUCCESSFUL, CONFIG_JOB_STREAMING, ID_JOB_STREAM
from database.db import get_db, DB
from streaming.generate.generate_main import generate_job_stream
from streaming.spark import Spark

scheduler = BackgroundScheduler({
    'apscheduler.job_defaults.max_instances': '10'
})


def get_job_stream():
    try:
        spark_properties = get_config(constants.CONFIG_SPARK)
        if spark_properties is None:
            return None
        spark_properties = spark_properties.value
        if spark_properties.get("name_job", None) is None:
            return JSONResponse(content={"message": "missing config for name spark job"},
                                status_code=status.HTTP_400_BAD_REQUEST)
        job = scheduler.get_job(job_id=ID_JOB_STREAM)
        dict_crontab = job.trigger.fields
        schedule = "{} {} {} {} {}".format(dict_crontab[CronTrigger.FIELD_NAMES.index("minute")],
                                           dict_crontab[CronTrigger.FIELD_NAMES.index("hour")],
                                           dict_crontab[CronTrigger.FIELD_NAMES.index("day")],
                                           dict_crontab[CronTrigger.FIELD_NAMES.index("month")],
                                           dict_crontab[CronTrigger.FIELD_NAMES.index("day_of_week")])
        return JSONResponse(content=dict(app_name=ID_JOB_STREAM, schedule=schedule, port=Spark().get_pid(),
                                         status="running" if is_process_running(Spark().get_pid(),
                                                                                "org.apache.spark.deploy.SparkSubmit") else "stopped"),
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content=dict(message="Error: {}".format(str(e))), status_code=status.HTTP_400_BAD_REQUEST)


def job_exec(db: DB, job_id: str, job_name: str):
    result_generate = generate_job_stream(db, job_name, job_id)
    if result_generate != GENERATE_STREAMING_SUCCESSFUL:
        return result_generate
    process_id = Spark().submit_job_spark(file="job_streaming_example")
    logging.info(f"submitting job in process: {process_id}")


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

        schedule = job_streaming_properties.get("schedule", None)
        if schedule is None:
            return "missing schedule for spark job"

        job = scheduler.get_job(job_id=ID_JOB_STREAM)
        if job is not None:
            scheduler.remove_job(job_id=ID_JOB_STREAM)
        scheduler.add_job(job_exec, CronTrigger.from_crontab(schedule), id=ID_JOB_STREAM, args=[db, ID_JOB_STREAM,
                                                                                                job_name])
        scheduler.start()
    except Exception as e:
        logging.error(e)
        return f"error {e}"
