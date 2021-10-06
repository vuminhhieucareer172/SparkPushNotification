import logging

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from streaming import settings


def connect_database():
    try:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        db = engine.connect()
        logging.info("connected to database with config:", engine.pool.status())
        return db
    except SQLAlchemyError as e:
        logging.error(e)
        return None
