from backend.models.dbstreaming_config import Config
from constants import constants
from database import session


def get_config_spark() -> Config:
    return session.query(Config).filter_by(name=constants.CONFIG_SPARK).scalar()


def get_config_kafka() -> Config:
    return session.query(Config).filter_by(name=constants.CONFIG_KAFKA).scalar()
