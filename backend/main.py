import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controller import table, database_connection
from backend.job_streaming.manage_job import init_scheduler, scheduler
from backend.schemas.database import Database
from database import db
from backend.schemas.table import Table

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/create-table/streaming")
async def create_table_streaming(new_schema: Table):
    return table.create_table_streaming(new_schema)


@app.post("/create-table/query")
async def create_table_query(new_schema: Table):
    return table.create_table(new_schema)


@app.post("/test-connect-database")
def test_connect_database(database_information: Database):
    return database_connection.test_connect_database(database_information)


@app.post("/connect-database")
def connect_database(database_information: Database):
    return database_connection.connect_database(database_information)


@app.on_event("shutdown")
async def shutdown_event():
    db.close()


if __name__ == '__main__':
    init_scheduler()
    uvicorn.run(app, host="0.0.0.0", port=5005)
    scheduler.shutdown(wait=False)
