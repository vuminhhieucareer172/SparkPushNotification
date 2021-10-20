import json
import logging
import time

from sqlalchemy import exc
from sqlalchemy.engine import reflection
from starlette.responses import JSONResponse
from starlette import status
from backend.models.dbstreaming_config import Config
from backend.schemas.configuration import Configuration, ConfigurationUpdate
from database import session, engine


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
                # print(inspector.get_columns(table))
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return []
    return table_detail

# def get_tables_by_name(table_name):
#     try:
#         de = session.query(Config).filter_by(id=config_id).scalar()
#     except exc.SQLAlchemyError as e:
#         logging.error(e)
#         return None
#     return config_record
