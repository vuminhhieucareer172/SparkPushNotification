import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse


from backend.controller import database_connection, query, configuration, tables_manager, stream, schedule
from backend.controller.schedule import init_scheduler, scheduler
from backend.schemas.configuration import Configuration, ConfigurationUpdate
from backend.schemas.database import Database
from backend.schemas.query import Query, QueryUpdate

from backend.schemas.stream import Stream, JobStream, TopicStream
from database.db import db

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add-stream")
async def add_stream(new_schema: Stream):
    return stream.add_stream(new_schema)


@app.post("/test-connect-database")
def test_connect_database(database_information: Database):
    return database_connection.test_connect_database(database_information)


@app.post("/connect-database")
def connect_database(database_information: Database):
    return database_connection.connect_database(database_information)


@app.get("/check-status-job-on-spark")
def check_status_spark():
    return stream.check_status_spark()


@app.on_event("shutdown")
async def shutdown_event():
    db.close()


@app.get("/query")
def get_query():
    return JSONResponse(query.get_query(), status_code=status.HTTP_200_OK)


@app.get("/query/{query_id}")
def get_query_by_id(query_id: int):
    return JSONResponse(query.get_query_by_id(query_id), status_code=status.HTTP_200_OK)


@app.post("/add-query")
def add_query(new_query: Query):
    return query.add_query(new_query)


@app.put("/update-query")
def update_query(new_query: QueryUpdate):
    return query.update_query(new_query)


@app.delete("/delete-query/{query_id}")
def delete_query(query_id: int):
    return query.delete_query(query_id)


@app.get("/config")
def get_config(skip: int = 0, limit: int = 10):
    return configuration.get_config(skip=skip, limit=limit)


@app.get("/config/{config_id}")
def get_config(config_id: int):
    return configuration.get_config_by_id(config_id)


@app.post("/add-config")
def add_config(new_config: Configuration):
    return configuration.add_config(new_config)


@app.put("/update-config")
def update_config(new_config: ConfigurationUpdate):
    return configuration.update_config(new_config)


@app.delete("/delete-config/{config_id}")
def delete_config(config_id: int):
    return configuration.delete_config(config_id)


@app.get("/tables")
def get_tables():
    return tables_manager.get_tables()
    # return JSONResponse(tables_manager.get_tables(), status_code=status.HTTP_200_OK)


@app.get("/tables/tables-detail/{table_name}")
def get_tables_by_name(table_name: str):
    return tables_manager.get_tables_by_name(table_name)


@app.get("/tables/table-record/{table_name}")
def get_tables_record(skip: int = 0, limit: int = 10):
    return configuration.get_config(skip=skip, limit=limit)


@app.get("/tables/stream")
def get_table_column(topic: TopicStream):
    return JSONResponse(tables_manager.get_tables_column(topic=topic), status_code=status.HTTP_200_OK)


@app.get("/job-streaming")
def job_streaming():
    return schedule.get_job_stream()


@app.get("/start-job-streaming")
def start_job_streaming():
    return stream.start_job_streaming()


@app.post("/update-job-streaming")
def update_job_streaming(new_schema_job: JobStream):
    return stream.update_job_streaming(new_schema_job)


@app.get("/stop-job-streaming")
def stop_job_streaming():
    return stream.stop_job_streaming()


if __name__ == '__main__':
    result_scheduler = init_scheduler()
    uvicorn.run(app, host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')))
    if scheduler.running:
        scheduler.shutdown()
