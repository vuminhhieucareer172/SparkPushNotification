from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette import status
from starlette.responses import JSONResponse

from backend.controller import stream, database_connection, query, configuration
from backend.schemas.configuration import Configuration, ConfigurationUpdate, ConfigurationGet
from backend.schemas.database import Database
from backend.schemas.query import Query, QueryUpdate
from backend.schemas.stream import Stream
from database import db
import os
from dotenv import load_dotenv

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


if __name__ == '__main__':
    uvicorn.run(app, host=os.getenv('APP_HOST'), port=int(os.getenv('APP_PORT')))
