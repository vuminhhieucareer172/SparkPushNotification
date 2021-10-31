import logging

import sqlalchemy
from fastapi import status
from sqlalchemy import exc, Column, Table, text, inspect
from sqlalchemy.engine import Inspector
from starlette.responses import JSONResponse

from backend.schemas import table
from constants.constants import PREFIX_DB_TABLE_STREAMING, DATA_TYPE_SQLALCHEMY, DATATYPE_STRING, \
    DATATYPE_NUMERIC, DATATYPE_DATE_AND_TIME
from database.db import meta, session, engine, db
from alembic import op


def convert_to_sqlalchemy(data_type: str):
    return DATA_TYPE_SQLALCHEMY.get(data_type.upper())


def add_column_to_table(table_instance: Table, new_columns: list):
    for field in new_columns:
        type_ = convert_to_sqlalchemy(field.type)
        if type_ in DATATYPE_STRING:
            if field.length is not None or field.length != 0:
                data_type = type_(field.length, collation=field.collation)
            else:
                data_type = type_(collation=field.collation)
            table_instance.append_column(Column(field.name_field, type_=data_type, primary_key=field.primary_key,
                                                nullable=field.nullable, server_default=field.default,
                                                comment=field.comment))
        elif type_ in DATATYPE_NUMERIC:
            if field.length is not None and field.length != 0:
                data_type = type_(field.length)
            else:
                data_type = type_
            if field.auto_increment:
                table_instance.append_column(Column(field.name_field, type_=data_type, primary_key=field.primary_key,
                                                    nullable=field.nullable, autoincrement=field.auto_increment,
                                                    comment=field.comment))
            elif field.default:
                table_instance.append_column(Column(field.name_field, type_=data_type, primary_key=field.primary_key,
                                                    nullable=field.nullable, server_default=field.default,
                                                    comment=field.comment))
        elif type_ in DATATYPE_DATE_AND_TIME:
            table_instance.append_column(
                Column(field.name_field, type_=type_, nullable=field.nullable,
                       server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment=field.comment))
        elif type_ == sqlalchemy.ARRAY:
            return JSONResponse(content="Not implemented", status_code=status.HTTP_501_NOT_IMPLEMENTED)
        elif type_ == sqlalchemy.JSON:
            table_instance.append_column(
                Column(field.name_field, type_=sqlalchemy.JSON, nullable=field.nullable, comment=field.comment))
        elif type_ == sqlalchemy.Enum:
            list_enum = field.value.split(', ')
            table_instance.append_column(
                Column(field.name_field, type_=sqlalchemy.Enum(*list_enum), nullable=field.nullable,
                       default=field.default, comment=field.comment))
        else:
            table_instance.append_column(
                Column(field.name_field, type_=type_, nullable=field.nullable, unique=field.unique,
                       default=field.default, comment=field.comment))
    return table_instance


def create_table(new_schema: table.Table, table_prefix_name=PREFIX_DB_TABLE_STREAMING) -> JSONResponse:
    try:
        new_table = Table(table_prefix_name + new_schema.name, meta, mysql_engine=new_schema.engine,
                          mysql_collate=new_schema.collate)
        new_table = add_column_to_table(table_instance=new_table, new_columns=new_schema.fields)
        new_table.create(checkfirst=True)
    except TypeError as e:
        return JSONResponse(content="TypeError: {}".format(e), status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        session.rollback()
        return JSONResponse(content="Failed with error {}".format(e), status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content="Table is created", status_code=status.HTTP_201_CREATED)


def update_table(new_schema: table.Table) -> JSONResponse:
    """
    support only drop columns
    :param new_schema:
    :return:
    """
    try:
        inspector: Inspector = inspect(engine)
        new_table = Table(new_schema.name, meta, autoload=True)
        columns: list = inspector.get_columns(new_schema.name)
        for column in columns:
            for field in new_schema.fields:
                if field.name_field == column.get('name'):
                    new_schema.fields.remove(field)
                    columns.remove(column)

        with db.connect() as conn:
            for column_drop in columns:
                rs = conn.execute('ALTER TABLE `{}` DROP COLUMN `{}`;'.format(new_schema.name, column_drop.get('name')))
                print(rs)
    except TypeError as e:
        return JSONResponse(content="TypeError: {}".format(e), status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        session.rollback()
        return JSONResponse(content="Failed with error {}".format(e), status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content="Table is created", status_code=status.HTTP_200_OK)
