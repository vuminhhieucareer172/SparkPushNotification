from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.controller import table
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


@app.on_event("shutdown")
async def shutdown_event():
    db.close()
