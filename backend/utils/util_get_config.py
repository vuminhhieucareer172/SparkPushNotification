import logging
from typing import Union

from sqlalchemy import exc

from backend.models.dbstreaming_config import Config
from constants import constants
from database import session


def get_config_spark() -> Union[Config, None]:
    try:
        return session.query(Config).filter_by(name=constants.CONFIG_SPARK).scalar()
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return None


def get_config_kafka() -> Union[Config, None]:
    try:
        return session.query(Config).filter_by(name=constants.CONFIG_KAFKA).scalar()
    except exc.SQLAlchemyError as e:
        logging.error(e)
        return None
