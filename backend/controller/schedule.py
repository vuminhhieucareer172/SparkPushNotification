import json
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from confluent_kafka import TopicPartition, Consumer
from dotenv import load_dotenv
from starlette import status
from starlette.responses import JSONResponse

from backend.models.dbstreaming_query import UserQuery
from backend.schemas.configuration import ConfigEmail, ConfigTelegram
from backend.schemas.query import Query
from backend.utils import util_mail, util_get_config, util_kafka, util_process, util_telegram
from constants import constants
from constants.constants import GENERATE_STREAMING_SUCCESSFUL, CONFIG_JOB_STREAMING, ID_JOB_STREAM
from database.db import get_db, DB, get_session
from database.session import SessionHandler
from streaming.generate.generate_main import generate_job_stream
from streaming.spark import Spark

scheduler = BackgroundScheduler({
    'apscheduler.job_defaults.max_instances': '10',
    'apscheduler.job_defaults.misfire_grace_time': '900',
})


def get_job_stream():
    try:
        spark_properties = util_get_config.get_config(constants.CONFIG_SPARK)
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
                                         status="running" if util_process.is_process_running(
                                             Spark().get_pid(), "org.apache.spark.deploy.SparkSubmit") else "stopped"),
                            status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content=dict(message="Error: {}".format(str(e))), status_code=status.HTTP_400_BAD_REQUEST)


def job_exec(db: DB, job_id: str, job_name: str):
    result_generate = generate_job_stream(db, job_name, job_id)
    if result_generate != GENERATE_STREAMING_SUCCESSFUL:
        print(result_generate)
        return
    process_id = Spark().submit_job_spark(file=ID_JOB_STREAM)
    logging.info(f"submitting job in process: {process_id}")


def init_scheduler():
    db = get_db()
    if db is None:
        return "Fail to connect database"
    job_streaming_properties = util_get_config.get_config(CONFIG_JOB_STREAMING)
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
        if not scheduler.running:
            scheduler.start()
        return "started scheduler"
    except Exception as e:
        logging.error(e)
        return f"Error {e}"


def add_job_output(new_query: Query):
    try:
        model_query = UserQuery(topic_kafka_output=new_query.topic_kafka_output, time_trigger=new_query.time_trigger,
                                contact=new_query.contact, sql=new_query.sql)
        scheduler.add_job(trigger_output, 'interval', seconds=int(new_query.time_trigger), args=[model_query],
                          id=new_query.topic_kafka_output)
        return JSONResponse(content=dict(message="ok"), status_code=status.HTTP_201_CREATED)
    except Exception as e:
        print(e)
        return JSONResponse(content=dict(message="Error: {}".format(str(e))), status_code=status.HTTP_400_BAD_REQUEST)


def update_job_output(new_query: Query):
    try:
        model_query = UserQuery(topic_kafka_output=new_query.topic_kafka_output, time_trigger=new_query.time_trigger,
                                contact=new_query.contact, sql=new_query.sql)
        scheduler.add_job(func=trigger_output, replace_existing=True, trigger='interval',
                          seconds=int(new_query.time_trigger), id=new_query.topic_kafka_output, args=[model_query])
        return JSONResponse(content=dict(message="ok"), status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content=dict(message="Error: {}".format(str(e))), status_code=status.HTTP_400_BAD_REQUEST)


def delete_job_output(job_id: str):
    try:
        scheduler.remove_job(job_id=job_id)
        return JSONResponse(content=dict(message="ok"), status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content=dict(message="Error: {}".format(str(e))), status_code=status.HTTP_400_BAD_REQUEST)


def trigger_output(new_query: UserQuery):
    try:
        consumer = Consumer(util_kafka.Kafka.create().get_credentials())
        consumer.subscribe([new_query.topic_kafka_output])

        topic = consumer.list_topics(topic=new_query.topic_kafka_output)
        partitions = [TopicPartition(new_query.topic_kafka_output, partition) for partition in
                      list(topic.topics[new_query.topic_kafka_output].partitions.keys())]

        committed_offset = consumer.committed(partitions)
        low, high = consumer.get_watermark_offsets(partitions[0])
        print("topic {} with offset is {}".format(new_query.topic_kafka_output, high))
        consumer.assign(committed_offset)

        data = []
        if committed_offset[0].offset < high:
            restart_time = 0
            while True:
                msg = consumer.poll(1)
                consumer.commit()

                if msg is None:
                    restart_time += 1
                    if restart_time > 10:
                        break
                    continue
                data.append(msg.value().decode('utf-8'))

                if msg.offset() == high - 1:
                    break
        handle_output(new_query, data)
    except Exception as e:
        print(e)
        raise e


def handle_output(new_query: UserQuery, data):
    try:
        if new_query.contact is None:
            pass
        else:
            contact_info: dict = new_query.contact
            result = None
            if 'method' not in contact_info:
                print('wrong format contact')
                return
            if contact_info.get('method') == constants.CONFIG_MAIL:
                mail_info = util_get_config.get_config(constants.CONFIG_MAIL).value
                result = util_mail.email_sender(
                    ConfigEmail(
                        host=mail_info.get('host'),
                        port=mail_info.get('port'),
                        email=mail_info.get('email'),
                        username=mail_info.get('username'),
                        password=mail_info.get('password'),
                        ssl=mail_info.get('ssl')
                    ), email_destination=contact_info.get('value'), subject='dbstreaming notify', content=data,
                    query=new_query)
            elif contact_info.get('method') == constants.CONFIG_TELEGRAM:
                telegram_info = util_get_config.get_config(constants.CONFIG_TELEGRAM).value
                result = util_telegram.send_test_message(
                    ConfigTelegram(token=telegram_info.get('token')),
                    chat_id=contact_info.get('value'),
                    message=json.dumps(data)
                )
            print('result of query {} sending to topic {}: {}'.format(new_query.id, new_query.topic_kafka_output, result))
    except Exception as e:
        print(e)
        raise e


def init_scheduler_from_query():
    try:
        db = get_db()
        session = get_session(database=db)
        query_session = SessionHandler.create(session, UserQuery)
        data = query_session.get_all()
        for query in data:
            scheduler.add_job(trigger_output, 'interval', seconds=int(query.time_trigger), args=[query],
                              id=query.topic_kafka_output)
        if not scheduler.running:
            scheduler.start()
    except Exception as e:
        print(e)
        return "Error {}".format(str(e))
