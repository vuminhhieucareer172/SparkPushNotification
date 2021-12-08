import datetime
import re
from typing import List

import sqlalchemy
from fastapi import status
from sqlalchemy import exc, Column, Table, text, inspect, MetaData
from sqlalchemy.engine import Inspector
from starlette.responses import JSONResponse

from backend.schemas import table
from backend.utils.util_kafka import get_latest_message
from constants import constants
from constants.constants import DATA_TYPE_SQLALCHEMY, DATATYPE_STRING, DATATYPE_NUMERIC, DATATYPE_DATE_AND_TIME
from database.db import DB, get_session


def convert_to_sqlalchemy(data_type: str):
    return DATA_TYPE_SQLALCHEMY.get(data_type.upper())


def add_column_to_table(table_instance: Table, new_columns: List[table.Field]):
    for field in new_columns:
        if not re.findall('^[a-zA-Z_][a-zA-Z0-9_]*$', field.name_field):
            return JSONResponse(content={"message": 'Error name column: ' + field.name_field}, status_code=status.HTTP_400_BAD_REQUEST)
        type_ = convert_to_sqlalchemy(field.type)
        if type_ in DATATYPE_STRING:
            if field.length is not None or field.length != 0:
                data_type = type_(field.length, collation=field.collation)
            else:
                data_type = type_(collation=field.collation)
            table_instance.append_column(Column(field.name_field, type_=data_type, primary_key=field.primary_key,
                                                nullable=not field.not_null, server_default=field.default,
                                                comment=field.comment))
        elif type_ in DATATYPE_NUMERIC:
            if field.auto_increment:
                table_instance.append_column(Column(field.name_field, type_=type_, primary_key=field.primary_key,
                                                    nullable=not field.not_null, autoincrement=field.auto_increment,
                                                    comment=field.comment))
            elif field.default:
                table_instance.append_column(Column(field.name_field, type_=type_, primary_key=field.primary_key,
                                                    nullable=not field.not_null, server_default=field.default,
                                                    comment=field.comment))
            else:
                table_instance.append_column(Column(field.name_field, type_=type_, primary_key=field.primary_key,
                                                    nullable=not field.not_null, comment=field.comment))
        elif type_ in DATATYPE_DATE_AND_TIME:
            if type_ == sqlalchemy.DATE:
                table_instance.append_column(
                    Column(field.name_field, type_=type_, nullable=not field.not_null, comment=field.comment))
            else:
                table_instance.append_column(
                    Column(field.name_field, type_=type_, nullable=not field.not_null,
                           server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), comment=field.comment))
        elif type_ == sqlalchemy.ARRAY:
            return JSONResponse(content={"message": "Not implemented"}, status_code=status.HTTP_501_NOT_IMPLEMENTED)
        elif type_ == sqlalchemy.JSON:
            table_instance.append_column(
                Column(field.name_field, type_=sqlalchemy.JSON, nullable=not field.not_null, comment=field.comment))
        elif type_ == sqlalchemy.Enum:
            list_enum = field.value.split(', ')
            table_instance.append_column(
                Column(field.name_field, type_=sqlalchemy.Enum(*list_enum), nullable=not field.not_null,
                       default=field.default, comment=field.comment))
        else:
            table_instance.append_column(
                Column(field.name_field, type_=type_, nullable=not field.not_null, unique=field.unique,
                       default=field.default, comment=field.comment))
    return table_instance


def create_table(new_schema: table.Table, db: DB) -> JSONResponse:
    session = get_session(database=db)
    try:
        new_table = Table(new_schema.name, MetaData(db.engine), mysql_engine=new_schema.engine,
                          mysql_collate=new_schema.collate)
        new_table = add_column_to_table(table_instance=new_table, new_columns=new_schema.fields)
        if not isinstance(new_table, Table):
            return new_table
        new_table.create(checkfirst=True)
    except TypeError as e:
        print(e)
        return JSONResponse(content={"message": "TypeError: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed with error {}".format(str(e))},
                            status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"message": "Table is created"}, status_code=status.HTTP_201_CREATED)


def update_table(new_schema: table.Table, db: DB) -> JSONResponse:
    """
    support only drop columns
    :param db:
    :param new_schema:
    :return:
    """
    session = get_session(database=db)
    try:
        inspector: Inspector = inspect(db.engine)
        new_table = Table(new_schema.name, MetaData(db.engine), autoload=True)
        columns: list = inspector.get_columns(new_schema.name)
        for column in columns:
            for field in new_schema.fields:
                if field.name_field == column.get('name'):
                    new_schema.fields.remove(field)
                    columns.remove(column)
        if columns:
            list_columns = []
            with db.connect() as conn:
                for column_drop in columns:
                    list_columns.append("`" + column_drop.get('name') + "`")
                conn.execute('ALTER TABLE `{}` DROP COLUMN {};'.format(new_schema.name, ', '.join(list_columns)))
    except TypeError as e:
        print(e)
        return JSONResponse(content={"message": "TypeError: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed with error {}".format(str(e))},
                            status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"message": "Table is created"}, status_code=status.HTTP_200_OK)


def get_schema_from_kafka_topic(topic: str):
    try:
        latest_mess, message = get_latest_message(topic=topic)
        if latest_mess == {}:
            return JSONResponse(content={"message": message}, status_code=status.HTTP_400_BAD_REQUEST)
        list_column = []
        data = {}
        for key_column in latest_mess.keys():
            type_column = ''
            if isinstance(latest_mess[key_column], str):
                type_column = 'TEXT'
            if isinstance(latest_mess[key_column], int):
                if -2147483648 <= latest_mess[key_column] <= 2147483648:
                    type_column = 'INTEGER'
                else:
                    type_column = 'LONG'
            if isinstance(latest_mess[key_column], float):
                type_column = 'FLOAT'
            try:
                date_time_obj = datetime.datetime.strptime(latest_mess[key_column], '%d/%m/%Y %H:%M:%S')
                if isinstance(date_time_obj, datetime.datetime):
                    type_column = 'DATETIME'
                date_time_obj = datetime.datetime.strptime(latest_mess[key_column], '%d/%m/%Y')
                if isinstance(date_time_obj, datetime.date):
                    type_column = 'DATE'
            except:
                pass
            column = {
                "name_field": key_column,
                "type": type_column,
            }
            list_column.append(column)
        print(1)
        data["message_sample"] = str(latest_mess)
        data["table"] = list_column
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def get_info_table(table_name: str, db: DB):
    table_info = dict(name=table_name, collate='', engine='InnoDB', fields=[])
    try:
        inspector: Inspector = inspect(db.engine)

        # get table option
        table_option = inspector.get_table_options(table_name=table_name)
        table_info['collate'] = table_option.get('mysql_collate', '')
        table_info['engine'] = table_option.get('mysql_engine')

        # get constraints
        list_primary_key = inspector.get_pk_constraint(table_name=table_name).get('constrained_columns', [])
        unique_constraints = inspector.get_unique_constraints(table_name=table_name)
        list_unique_column = list(map(lambda x: x.get('column_names')[0], unique_constraints))

        # get columns
        list_columns: List[dict] = inspector.get_columns(table_name=table_name)
        for column in list_columns:
            new_column = dict(name_field=column.get('name'), type='VARCHAR', length=None, value=None, primary_key=False,
                              not_null=not column.get('nullable', True), unique=False, default=column.get('default'),
                              auto_increment=column.get('autoincrement', False),
                              collation=None, comment=column.get('comment'))
            if column.get('name') in list_primary_key:
                new_column['primary_key'] = True
            if column.get('name') in list_unique_column:
                new_column['unique'] = True

            for key in constants.DATA_TYPE_SQLALCHEMY.keys():
                if isinstance(column.get('type'), constants.DATA_TYPE_SQLALCHEMY[key]):
                    new_column['type'] = key
                    if constants.DATA_TYPE_SQLALCHEMY[key] in constants.DATATYPE_STRING:
                        new_column['length'] = column.get('type').__dict__.get('length', None)
                        new_column['collation'] = column.get('type').__dict__.get('collation', None)
                    elif constants.DATA_TYPE_SQLALCHEMY[key] in constants.DATATYPE_NUMERIC:
                        new_column['length'] = column.get('type').__dict__.get('display_width', None)

            table_info.get('fields').append(new_column)
        return table_info
    except Exception as e:
        print(e)
        raise e
