import json
import logging
import time

from sqlalchemy import exc
from sqlalchemy.engine import reflection
from starlette.responses import JSONResponse
from starlette import status
from backend.models.dbstreaming_config import Config
from backend.schemas.configuration import Configuration, ConfigurationUpdate
from backend.schemas.stream import TopicStream
from database import session, engine
from streaming.utils.util_kafka import get_latest_message


def get_tables():
    try:
        # tables_name = engine.execute('SHOW TABLES').fetchall()
        # tables_name = engine.table_names()
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


def get_tables_column(topic: TopicStream):
    try:
        lastest_mess = json.loads(get_latest_message(topic=topic.topic_kafka_input))
        table = []
        for key_column in lastest_mess.keys():
            type_column = ''
            if isinstance(lastest_mess[key_column], str):
                type_column = 'VARCHAR'
            if isinstance(lastest_mess[key_column], int):
                if -2147483648 <= lastest_mess[key_column] <= 2147483648:
                    type_column = 'INTEGER'
                else:
                    type_column = 'LONG'
            if isinstance(lastest_mess[key_column], float):
                type_column = 'FLOAT'

            column = {
                "name_field": key_column,
                "collation": "latin1_swedish_ci",
                "type": type_column,
                "comment": None
            }
            table.append(column)
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return []
    return table
