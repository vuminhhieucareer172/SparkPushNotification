import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controller import stream, database_connection, query
from backend.job_streaming.manage_job import init_scheduler, scheduler
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


if __name__ == '__main__':
    init_scheduler()
    uvicorn.run(app, host="0.0.0.0", port=5005)
    scheduler.shutdown(wait=False)
