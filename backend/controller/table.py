import logging

import sqlalchemy
from fastapi import status
from sqlalchemy import exc, Column, Table, text
from starlette.responses import JSONResponse

from backend.schemas import table
from constants.constants import PREFIX_DB_TABLE_QUERY, PREFIX_DB_TABLE_STREAMING, DATA_TYPE_SQLALCHEMY, DATATYPE_STRING, \
    DATATYPE_NUMERIC, DATATYPE_DATE_AND_TIME
from database import meta


def convert_to_sqlalchemy(data_type: str):
    return DATA_TYPE_SQLALCHEMY.get(data_type.upper())


def create_table(new_schema: table.Table, table_prefix_name=PREFIX_DB_TABLE_QUERY):
    try:
        new_table = Table(table_prefix_name + new_schema.name, meta, mysql_engine=new_schema.engine,
                          mysql_default_charset=new_schema.charset, mysql_collate=new_schema.collate)

        primary = new_schema.fields.primary

        new_table.append_column(Column(primary.name_field, type_=convert_to_sqlalchemy(primary.type), primary_key=True,
                                       index=True, autoincrement=primary.auto_increment, comment=primary.comment))

        for other in new_schema.fields.others:
            type_ = convert_to_sqlalchemy(other.type)
            if type_ in DATATYPE_STRING:
                if other.length is not None or other.length != 0:
                    data_type = type_(other.length, collation=other.collation)
                else:
                    data_type = type_(collation=other.collation)
                new_table.append_column(Column(other.name_field, type_=data_type, nullable=other.nullable,
                                               server_default=other.default, comment=other.comment))
            elif type_ in DATATYPE_NUMERIC:
                if other.length is not None or other.length != 0:
                    data_type = type_(other.length)
                else:
                    data_type = type_
                new_table.append_column(Column(other.name_field, type_=data_type, nullable=other.nullable,
                                               server_default=other.default, comment=other.comment))
            elif type_ in DATATYPE_DATE_AND_TIME:
                new_table.append_column(
                    Column(other.name_field, type_=type_, nullable=other.nullable,
                           server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'),
                           comment=other.comment))
            elif type_ == sqlalchemy.ARRAY:
                return JSONResponse(content="Not implemented", status_code=status.HTTP_501_NOT_IMPLEMENTED)
            elif type_ == sqlalchemy.JSON:
                new_table.append_column(
                    Column(other.name_field, type_=sqlalchemy.JSON, nullable=other.nullable, comment=other.comment))
            elif type_ == sqlalchemy.Enum:
                list_enum = other.value.split(', ')
                new_table.append_column(
                    Column(other.name_field, type_=sqlalchemy.Enum(*list_enum), nullable=other.nullable,
                           default=other.default, comment=other.comment))
            else:
                new_table.append_column(
                    Column(other.name_field, type_=type_, nullable=other.nullable, unique=other.unique,
                           default=other.default, comment=other.comment))
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
