import logging

from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import exc
from starlette.responses import JSONResponse

from database import db
from schemas.table import Table

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
    print(new_schema)
    try:
        sql = "CREATE TABLE {} (".format(new_schema.name)
        primary = new_schema.fields.primary
        sql += "{} {} PRIMARY KEY {}".format(
            primary.name_field, primary.type, "AUTO_INCREMENT" if primary.auto_increment else ""
        )
        for other in new_schema.fields.others:
            sql += ", {} {} {} {} {}".format(
                other.name_field, other.type, "NOT NULL" if not other.nullable else "",
                "UNIQUE" if other.unique else "", "DEFAULT '" + other.default + "'" if other.default != "" else ""
            )

        sql += ") ENGINE={} CHARACTER SET {} COLLATE {}".format(new_schema.engine, new_schema.character_set,
                                                                new_schema.collate)
        print(sql)
        db.execute(sql)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return JSONResponse(content="Failed", status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content="Table is created", status_code=status.HTTP_201_CREATED)


@app.on_event("shutdown")
async def shutdown_event():
    db.close()
