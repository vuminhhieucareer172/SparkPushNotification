import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from backend.controller import database_connection, query, configuration, table, stream, schedule
from backend.controller.schedule import init_scheduler, scheduler
from backend.middleware.database import verify_database
from backend.schemas.configuration import ConfigurationUpdate
from backend.schemas.database import Database
from backend.schemas.query import Query, QueryUpdate
from backend.schemas.stream import Stream, JobStream, KafkaTopic
from backend.utils import util_kafka
from backend.utils.util_kafka import get_list_topics
from database.db import DB
from streaming import spark
from pathlib import Path
Path("logs").mkdir(parents=True, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/static/log-job-dbstreaming', StaticFiles(directory='logs'), name='log-job-dbstreaming')


@app.post("/test-connect-database")
def test_connect_database(database_information: Database):
    is_connectable = database_connection.test_connect_database(database_information)
    if is_connectable:
        return JSONResponse(content={"message": "Connect successfully"}, status_code=status.HTTP_202_ACCEPTED)
    return JSONResponse(content={"message": "cannot to connect db"}, status_code=status.HTTP_400_BAD_REQUEST)


@app.post("/connect-database")
def connect_database(database_information: Database):
    return database_connection.connect_database(database_information)


@app.get("/connect-database")
def get_config_connect_database():
    return database_connection.get_config_connect_database()


@app.get("/stream")
def get_all_stream(db=Depends(verify_database)):
    return stream.get_all_stream(db)


@app.get("/stream/{stream_name}")
def get_stream(stream_name: str, db=Depends(verify_database)):
    return stream.get_stream_by_name(stream_name, db)


@app.get("/stream/record/{stream_name}")
def get_stream_record(stream_name: str, db=Depends(verify_database)):
    return stream.get_record_by_stream_name(stream_name, db)


@app.post("/add-stream")
def add_stream(new_schema: Stream, db=Depends(verify_database)):
    return stream.add_stream(new_schema, db)


@app.put("/update-stream")
def update_stream(update_schema: Stream, db=Depends(verify_database)):
    return stream.update_stream(update_schema, db)


@app.delete("/stream/{name}")
def delete_stream(name: str, db=Depends(verify_database)):
    return stream.delete_stream(name, db)


@app.get("/check-status-job-on-spark")
def check_status_spark(db=Depends(verify_database)):
    return stream.check_status_spark(db)


@app.get("/status-spark")
def status_spark(db=Depends(verify_database)):
    return spark.status_spark(db)


@app.get("/status-kafka")
def status_kafka(db=Depends(verify_database)):
    return util_kafka.check_status(db)


@app.get("/status-mysql")
def status_mysql():
    return database_connection.status_mysql()


@app.get("/query")
def get_query(skip: int = 0, limit: int = 10000, db=Depends(verify_database)):
    return query.get_query(db, skip, limit)


@app.get("/query/{query_id}")
def get_query_by_id(query_id: int, db=Depends(verify_database)):
    return query.get_query_by_id(query_id, db)


@app.post("/query")
def add_query(new_query: Query, db=Depends(verify_database)):
    return query.add_query(new_query, db)


@app.put("/update-query")
def update_query(new_query: QueryUpdate, db=Depends(verify_database)):
    return query.update_query(new_query, db)


@app.delete("/query/{query_id}")
def delete_query(query_id: int, db=Depends(verify_database)):
    return query.delete_query(query_id, db)


@app.get("/config")
def get_config(skip: int = 0, limit: int = 10, db=Depends(verify_database)):
    return configuration.get_config(db, skip=skip, limit=limit)


@app.get("/config/{config_name}")
def get_config(config_name: str, db=Depends(verify_database)):
    return configuration.get_config_by_name(config_name, db)


@app.put("/config")
def update_config(new_config: ConfigurationUpdate, db=Depends(verify_database)):
    return configuration.update_config(new_config, db)


@app.get("/kafka-topic/{topic}")
def get_schema_from_kafka_topic(topic: str, db=Depends(verify_database)):
    return table.get_schema_from_kafka_topic(topic=topic)


@app.get("/kafka-topic")
def get_list_kafka_topics(db=Depends(verify_database)):
    list_topic_kafka = get_list_topics()
    if isinstance(list_topic_kafka, str):
        return JSONResponse(list_topic_kafka, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(list_topic_kafka, status_code=status.HTTP_200_OK)


@app.post("/kafka-topic/create")
def create_kafka_topic(schema_topic: KafkaTopic, db=Depends(verify_database)):
    return util_kafka.create_topic(schema_topic)


@app.get("/job-streaming")
def job_streaming():
    return schedule.get_job_stream()


@app.get("/start-job-streaming")
def start_job_streaming():
    return stream.start_job_streaming()


@app.post("/update-job-streaming")
def update_job_streaming(new_schema_job: JobStream, db=Depends(verify_database)):
    return stream.update_job_streaming(new_schema_job, db)


@app.get("/stop-job-streaming")
def stop_job_streaming():
    return stream.stop_job_streaming()


@app.on_event("startup")
async def startup_event():
    result_scheduler = init_scheduler()
    if isinstance(result_scheduler, str):
        print(result_scheduler)


@app.on_event("shutdown")
async def shutdown_event():
    DB().close()
    if scheduler.running:
        scheduler.shutdown()


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run("backend.main:app", host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')),
                reload=bool(os.getenv('DEV_ENV')))
