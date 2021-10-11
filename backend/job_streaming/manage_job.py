from datetime import datetime
from apscheduler.triggers.cron import CronTrigger

from backend.models.job import JobStream
from constants import constants
from apscheduler.schedulers.background import BackgroundScheduler
from database import session
from streaming.generate import generate_main

scheduler = BackgroundScheduler({
    'apscheduler.job_defaults.max_instances': '20'
})


def job_exec(job_id, func):
    job = session.query(JobStream).filter_by(id=job_id).first()
    job.status = constants.JOB_STREAMING_STATUS_RUNNING
    job.log = ''
    try:
        session.commit()
    except Exception as error:
        print(error)
    log = 'this is log'
    if log != '':
        job.status = constants.JOB_STREAMING_STATUS_ERROR
        job.log = log
        print(log)
    else:
        job.status = constants.JOB_STREAMING_STATUS_STOP
    try:
        session.commit()
    except Exception as error:
        print(error)
    session.close()


def init_scheduler():
    jobs = session.query(JobStream).all()
    for job in jobs:
        if job.enabled:
            scheduler.add_job(job_exec, CronTrigger.from_crontab(job.time), args=[job.id, job.template])
    scheduler.start()
    for e in scheduler.get_jobs():
        e.modify(next_run_time=datetime.now())
