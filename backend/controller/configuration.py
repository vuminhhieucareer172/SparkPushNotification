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
        config_record = config_session.get_one(query_dict=dict(name=config_name))
        if config_record is not None:
            config_record = config_session.to_json(config_record)
        return JSONResponse(config_record,
                            status_code=status.HTTP_200_OK)
    except exc.SQLAlchemyError as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def update_config(new_config: ConfigurationUpdate, db: DB):
    session = get_session(database=db)
    try:
        config_session = SessionHandler.create(session, Config)
        config_record = config_session.get_one(query_dict=dict(name=new_config.name))
        if config_record is None:
            config_session.add(new_config.dict())
            session.commit()
        else:
            config_record.name = new_config.name
            config_record.value = new_config.value
            session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)


