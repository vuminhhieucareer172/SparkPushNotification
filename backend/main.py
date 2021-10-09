from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controller import stream
from backend.controller.table import create
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


@app.post("/create-table")
async def create_table(new_schema: Table):
    return create(new_schema)


@app.get("/spark-version")
def get_version_of_spark():
    return stream.spark_version()


@app.get("/job-stream")
def get_job_stream():
    return stream.get_list_applications()


@app.on_event("shutdown")
async def shutdown_event():
    db.close()
