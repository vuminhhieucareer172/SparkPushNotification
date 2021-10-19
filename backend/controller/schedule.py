import logging
import os

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from dotenv import load_dotenv
from unidecode import unidecode

from backend.controller.stream import submit_job_spark
from backend.utils.util_get_config import get_config_spark
from constants.constants import GENERATE_STREAMING_SUCCESSFUL
from streaming.generate.generate_main import generate_job_stream
from streaming.spark import spark

scheduler = BackgroundScheduler({
    'apscheduler.job_defaults.max_instances': '10'
})


def job_exec(job_id: str, job_name: str):
    result_generate = generate_job_stream(job_name, job_id)
    if result_generate != GENERATE_STREAMING_SUCCESSFUL:
        return result_generate
    process = submit_job_spark(job_id)
    logging.info(f"submitting job in process: {process.pid}")


def generate_job_id(name: str):
    res = unidecode(name).lower().strip()
    return '_'.join(res.split())


def init_scheduler():
    spark_properties = get_config_spark()
    if spark_properties is None:
        return "missing spark config"
    spark_properties = spark_properties.value
    try:
        load_dotenv()

        job_name = spark_properties.get("name_job", None)
        if job_name is None:
            return "missing config for name spark job"
        job_id = generate_job_id(spark_properties.get("name_job"))
        schedule = os.getenv("STREAMING_SCHEDULE")
        job = scheduler.get_job(job_id=job_id)
        if job is not None:
            scheduler.remove_job(job_id=job_id)
        scheduler.add_job(job_exec, CronTrigger.from_crontab(schedule), id=job_id, args=[job_id, job_name])
        scheduler.start()
    except Exception as e:
        logging.error(e)
        return f"error {e}"
