import logging

from sqlalchemy import exc
from starlette.responses import JSONResponse
from fastapi import status
from backend.database import db
from backend.schemas.table import Table


def create(new_schema: Table):
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
