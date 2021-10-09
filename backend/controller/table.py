import logging

from fastapi import status
from sqlalchemy import exc, Column, Table, VARCHAR, INTEGER, TEXT, DATETIME, TIMESTAMP, DATE, ARRAY, func, text
from starlette.responses import JSONResponse

from backend.schemas import table
from constants.constants import PREFIX_DB_TABLE_QUERY, PREFIX_DB_TABLE_STREAMING
from database import meta

to_type_sqlalchemy = {
    "VARCHAR": VARCHAR,
    "INTEGER": INTEGER,
    "TEXT": TEXT,
    "DATETIME": DATETIME,
    "TIMESTAMP": TIMESTAMP,
    "DATE": DATE,
    "FLOAT": VARCHAR,
    "ARRAY": ARRAY
}


def convert_to_sqlalchemy(data_type: str):
    return to_type_sqlalchemy.get(data_type)


def create_table(new_schema: table.Table, table_prefix_name=PREFIX_DB_TABLE_QUERY):
    try:
        new_table = Table(table_prefix_name + new_schema.name, meta, mysql_engine=new_schema.engine,
                          mysql_default_charset=new_schema.charset, mysql_collate=new_schema.collate)

        primary = new_schema.fields.primary

        new_table.append_column(Column(primary.name_field, type_=convert_to_sqlalchemy(primary.type), primary_key=True,
                                       index=True, autoincrement=primary.auto_increment, comment=primary.comment))

        for other in new_schema.fields.others:
            type_ = convert_to_sqlalchemy(other.type)
            if other.length is not None or other.length != 0:
                type_ = convert_to_sqlalchemy(other.type)(other.length)
            if other.type in ["TIMESTAMP"]:
                other.collation = None
                new_table.append_column(
                    Column(other.name_field, type_=type_, nullable=other.nullable,
                           unique=other.unique, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                           comment=other.comment))

            else:
                new_table.append_column(
                    Column(other.name_field, type_=type_, nullable=other.nullable,
                           unique=other.unique, default=other.default, comment=other.comment))
        new_table.create()
    except TypeError as e:
        return JSONResponse(content="TypeError: {}".format(e), status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return JSONResponse(content="Failed with error {}".format(e), status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content="Table is created", status_code=status.HTTP_201_CREATED)


def create_table_streaming(new_schema: table.Table):
    require_field = ['sql', 'created_at', 'time_trigger', 'updated_at']
    for field in new_schema.fields.others:
        if field.name_field in require_field:
            require_field.remove(field.name_field)
    if len(require_field) > 0:
        return JSONResponse(content="missing required field " + ", ".join(require_field),
                            status_code=status.HTTP_400_BAD_REQUEST)
    return create_table(new_schema, table_prefix_name=PREFIX_DB_TABLE_STREAMING)
