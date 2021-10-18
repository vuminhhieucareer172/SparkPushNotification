from sqlalchemy import Column, Enum, INTEGER, JSON

from backend.schemas.configuration import Configuration
from constants import constants
from database import Model


class Config(Model):
    __tablename__ = "dbstreaming_config"

    id = Column(INTEGER, primary_key=True, index=True, autoincrement=True)
    name = Column(Enum(constants.CONFIG_SPARK, constants.CONFIG_MAIL, constants.CONFIG_KAFKA, constants.CONFIG_ZALO),
                  nullable=False)
    value = Column(JSON, nullable=False)

    def __init__(self, **kwargs):
        super(Config, self).__init__(**kwargs)

    def to_full_json(self):
        return dict(
            id=self.id,
            name=self.name,
            value=self.value,
        )

    @staticmethod
    def from_json(schemas_config: Configuration):
        return Config(
            name=schemas_config.name,
            value=schemas_config.value,
        )