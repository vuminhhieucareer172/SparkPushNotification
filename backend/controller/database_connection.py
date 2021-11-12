import dotenv
from fastapi import status
from sqlalchemy import create_engine, exc
from starlette.responses import JSONResponse

from backend.schemas import database
from database.db import DB


def test_connect_database(schema_database: database.Database):
    """
    db_driver:{"postgresql","mysql","mssql"}
    """
    try:
        engine = create_engine(
            '{}://{}:{}@{}:{}/{}?driver={}'.format(schema_database.db_driver,
                                                   schema_database.db_username,
                                                   schema_database.db_password,
                                                   schema_database.db_host,
                                                   schema_database.db_port,
                                                   schema_database.db_name,
                                                   schema_database.db_driver_manager))
        engine.connect()
    except exc.OperationalError as e:
        print(e)
        return False
    return True


def connect_database(schema_database: database.Database):
    connectable = test_connect_database(schema_database)
    try:
        if connectable:
            dotenv_file = dotenv.find_dotenv()
            dotenv.load_dotenv(dotenv_file, override=True)
            for info in schema_database:
                dotenv.set_key(dotenv_file, info[0].upper(), str(info[1]))
            db = DB.create()
            db.re_create_engine()
        else:
            return JSONResponse(content={"message": "Cannot connect to database"}, status_code=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        return JSONResponse(content={"message": str(e)}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"message": "Connect successfully"}, status_code=status.HTTP_202_ACCEPTED)


def get_config_connect_database():
    try:
        return JSONResponse(content=DB.get_credentials(), status_code=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return JSONResponse(content=e, status_code=status.HTTP_400_BAD_REQUEST)


def status_mysql():
    try:
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)
        db = DB.create()
        db.connect()
    except Exception as e:
        print(e)
        return JSONResponse(content={"status": "stopped", "message": "cannot connect to kafka with config {}".format(
            DB.get_credentials()
        )}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={"status": "running"}, status_code=status.HTTP_200_OK)
