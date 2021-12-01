import os

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controller import schedule
from backend.controller.schedule import scheduler
from backend.models.dbstreaming_query import UserQuery
from backend.schemas.query import Query
from database.db import DB

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/add-job-output")
def add_output(new_query: Query):
    return schedule.add_job_output(new_query)


@app.put("/update-job-output")
def update_output(new_query: Query):
    return schedule.update_job_output(new_query)


@app.delete("/delete-job-output/{job_id: str}")
def delete_output(job_id: str):
    return schedule.delete_job_output(job_id)


@app.on_event("startup")
async def startup_event():
    schedule.init_scheduler_from_query()


@app.on_event("shutdown")
async def shutdown_event():
    DB().close()
    if scheduler.running:
        scheduler.shutdown()


if __name__ == '__main__':
    load_dotenv()
    uvicorn.run("backend.output.main_scheduler:app", host=os.getenv('APP_HOST'), port=int(os.getenv('APP_OUTPUT_PORT')),
                reload=bool(os.getenv('DEV_ENV')))
