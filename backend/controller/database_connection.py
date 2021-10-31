import logging

import dotenv
from fastapi import status
from sqlalchemy import create_engine, exc
from starlette.responses import JSONResponse

from backend.schemas import database
from database.db import DB


def test_connect_database(schema_database: database.Database):
    try:
        engine = create_engine(
            '{}://{}:{}@{}:{}/{}'.format(schema_database.db_driver, schema_database.db_username,
                                         schema_database.db_password, schema_database.db_host, schema_database.db_port,
                                         schema_database.db_name))
        engine.connect()
    except exc.OperationalError as e:
        logging.error(e)
        return False
    return True


def connect_database(schema_database: database.Database):
    connectable = test_connect_database(schema_database)
    try:
        if connectable:
            dotenv_file = dotenv.find_dotenv()
            dotenv.load_dotenv(dotenv_file)
            for info in schema_database:
                dotenv.set_key(dotenv_file, info[0].upper(), str(info[1]))
        else:
            return JSONResponse(content="Cannot connect to database", status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logging.error(e)
        return JSONResponse(content=e, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content="Connect successfully", status_code=status.HTTP_202_ACCEPTED)


def get_config_connect_database():
    try:
        return JSONResponse(content=DB.get_credentials(), status_code=status.HTTP_200_OK)
    except Exception as e:
        logging.error(e)
        return JSONResponse(content=e, status_code=status.HTTP_400_BAD_REQUEST)
