import datetime
import logging
from datetime import datetime

from sqlalchemy import exc
from sqlalchemy.engine import reflection
from starlette import status
from starlette.responses import JSONResponse

from database.db import engine
from backend.utils.util_kafka import get_latest_message


def get_tables():
    try:
        inspector = reflection.Inspector.from_engine(engine)
        tables_name = inspector.get_table_names()
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return []
    return tables_name


def get_tables_by_name(table_name: str):
    try:
        inspector = reflection.Inspector.from_engine(engine)
        for table in inspector.get_table_names():
            if table == table_name:
                table_detail = inspector.get_columns(table)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return []
    return table_detail


def get_tables_column(topic: str):
    try:
        latest_mess, message = get_latest_message(topic=topic)
        if latest_mess == {}:
            return JSONResponse(content=message, status_code=status.HTTP_400_BAD_REQUEST)
        table = []
        data = {}
        for key_column in latest_mess.keys():
            type_column = ''
            if isinstance(latest_mess[key_column], str):
                type_column = 'VARCHAR'
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
            except:
                pass
            column = {
                "name_field": key_column,
                "type": type_column,
            }
            table.append(column)
        data["message_sample"] = str(latest_mess)
        data["table"] = table
        return JSONResponse(content=data, status_code=status.HTTP_200_OK)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return JSONResponse(content={"message": "Failed", "detail": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
