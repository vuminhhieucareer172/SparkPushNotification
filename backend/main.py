import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controller import stream, database_connection, query, configuration
# from backend.job_streaming.manage_job import init_scheduler, scheduler
from backend.schemas.configuration import Configuration, ConfigurationUpdate
from backend.schemas.database import Database
from backend.schemas.query import Query, QueryUpdate
from backend.schemas.stream import Stream
from database import db

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


@app.post("/add-config")
def add_config(new_config: Configuration):
    return configuration.add_config(new_config)


@app.put("/update-config")
def update_query(new_config: ConfigurationUpdate):
    return configuration.update_config(new_config)

@app.delete("/delete-config/{config_id}")
def delete_query(config_id: int):
    return configuration.delete_config(config_id)

if __name__ == '__main__':
    # init_scheduler()
    uvicorn.run(app, host="0.0.0.0", port=5005)
    # scheduler.shutdown(wait=False)
