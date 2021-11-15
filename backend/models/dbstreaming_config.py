from sqlalchemy import Column, Enum, INTEGER, JSON
from sqlalchemy.ext.declarative import declarative_base

from constants import constants

Model = declarative_base()


class Config(Model):
    __tablename__ = "dbstreaming_config"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    name = Column(Enum(constants.CONFIG_SPARK, constants.CONFIG_MAIL, constants.CONFIG_KAFKA, constants.CONFIG_ZALO,
                       constants.CONFIG_JOB_STREAMING, constants.CONFIG_TELEGRAM),
                  nullable=False, unique=True)
    value = Column(JSON, nullable=False)

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)
