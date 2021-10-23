import logging
from typing import Union

from sqlalchemy import exc

from backend.models.dbstreaming_config import Config
from database.db import session


def get_config(type_config: str) -> Union[Config, None]:
    try:
        return session.query(Config).filter_by(name=type_config).scalar()
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return None
