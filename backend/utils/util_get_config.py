import logging
from typing import Union

from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from backend.models.dbstreaming_config import Config
from database.db import DB
from database.session import SessionHandler


def get_config(type_config: str) -> Union[Config, None]:
    try:
        db = DB.create()
        engine = db.engine
        if engine is None:
            return None
        Session = sessionmaker(bind=engine)
        session = Session()
        config_session = SessionHandler.create(session, Config)
        return config_session.get_one(dict(name=type_config))
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return None
