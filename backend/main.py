import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from backend.controller import database_connection, query, configuration, tables_manager, stream, schedule
from backend.controller.schedule import init_scheduler, scheduler
from backend.middleware.database import verify_database
from backend.schemas.configuration import Configuration, ConfigurationUpdate
from backend.schemas.database import Database
from backend.schemas.query import Query, QueryUpdate
from backend.schemas.stream import Stream, JobStream
from backend.utils import util_kafka
from backend.utils.util_kafka import get_list_topics
from database.db import DB
from streaming import spark

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/test-connect-database")
def test_connect_database(database_information: Database):
    return database_connection.test_connect_database(database_information)


@app.post("/connect-database")
def connect_database(database_information: Database):
    return database_connection.connect_database(database_information)


@app.get("/connect-database")
def get_config_connect_database():
    return database_connection.get_config_connect_database()


@app.get("/stream")
def get_all_stream(db=Depends(verify_database)):
    pass


@app.get("/stream/{name: str}")
def get_stream(name: str, db=Depends(verify_database)):
    pass


@app.post("/stream")
def add_stream(new_schema: Stream, db=Depends(verify_database)):
    return stream.add_stream(new_schema, db)


@app.put("/stream")
def update_stream(update_schema: Stream, db=Depends(verify_database)):
    return stream.update_stream(update_schema, db)


@app.delete("/stream/{name: str}")
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
def get_query(skip: int = 0, limit: int = 10, db=Depends(verify_database)):
    return JSONResponse(query.get_query(db, skip, limit), status_code=status.HTTP_200_OK)


@app.get("/query/{query_id}")
def get_query_by_id(query_id: int, db=Depends(verify_database)):
    return JSONResponse(query.get_query_by_id(query_id, db), status_code=status.HTTP_200_OK)


@app.post("/query")
def add_query(new_query: Query, db=Depends(verify_database)):
    return query.add_query(new_query, db)


@app.put("/query")
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


@app.post("/config")
def add_config(new_config: Configuration, db=Depends(verify_database)):
    return configuration.add_config(new_config, db)


@app.put("/config")
def update_config(new_config: ConfigurationUpdate, db=Depends(verify_database)):
    return configuration.update_config(new_config, db)


@app.delete("/config/{config_id}")
def delete_config(config_id: int, db=Depends(verify_database)):
    return configuration.delete_config(config_id, db)


@app.get("/tables")
def get_tables(db=Depends(verify_database)):
    return tables_manager.get_tables(db)


@app.get("/tables/tables-detail/{table_name}")
def get_tables_by_name(table_name: str, db=Depends(verify_database)):
    return tables_manager.get_tables_by_name(table_name, db)


@app.get("/tables/table-record/{table_name}")
def get_tables_record(skip: int = 0, limit: int = 10, db=Depends(verify_database)):
    return configuration.get_config(db, skip=skip, limit=limit)


@app.get("/kafka-topic/{topic}")
def get_table_column(topic: str, db=Depends(verify_database)):
    return tables_manager.get_tables_column(topic=topic)


@app.get("/kafka-topic")
def get_table_column(db=Depends(verify_database)):
    list_topic_kafka = get_list_topics()
    if isinstance(list_topic_kafka, str):
        return JSONResponse(list_topic_kafka, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(list_topic_kafka, status_code=status.HTTP_200_OK)


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
