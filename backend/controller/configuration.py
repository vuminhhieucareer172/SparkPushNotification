import logging

from sqlalchemy import exc
from starlette import status
from starlette.responses import JSONResponse

from backend.models.dbstreaming_config import Config
from backend.schemas.configuration import Configuration, ConfigurationUpdate
from database.db import DB, get_session
from database.session import SessionHandler


def get_config(db: DB, skip: int = 0, limit: int = 10):
    try:
        session = get_session(database=db)
        config_session = SessionHandler.create(session, Config)
        return JSONResponse(config_session.get_from_offset(skip, limit, to_json=True), status_code=status.HTTP_200_OK)
    except exc.SQLAlchemyError as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def get_config_by_name(config_name: str, db: DB):
    try:
        session = get_session(database=db)
        config_session = SessionHandler.create(session, Config)
        return JSONResponse(config_session.get_one(query_dict=dict(name=config_name), to_json=True),
                            status_code=status.HTTP_200_OK)
    except exc.SQLAlchemyError as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def add_config(new_config: Configuration, db: DB):
    session = get_session(database=db)
    try:
        config_session = SessionHandler.create(session, Config)
        config_session.add(new_config.dict())
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed"}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def update_config(new_config: ConfigurationUpdate, db: DB):
    session = get_session(database=db)
    try:
        config_session = SessionHandler.create(session, Config)
        config_record = config_session.get(_id=new_config.id)
        if config_record is None:
            return JSONResponse(content={"message": "Not found config"}, status_code=status.HTTP_404_NOT_FOUND)
        config_record.name = new_config.name
        config_record.value = new_config.value
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)


def delete_config(config_id: int, db: DB):
    session = get_session(database=db)
    try:
        config_session = SessionHandler.create(session, Config)
        config_session.delete(dict(id=config_id))
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)
