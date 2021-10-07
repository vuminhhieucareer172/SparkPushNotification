import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# db mysql
from constants import constants

engine = create_engine(
    constants.SQLALCHEMY_DATABASE_URI, **constants.SQLALCHEMY_ENGINE_OPTIONS
)
db = engine.connect()
logging.info("connected to database with config:", engine.pool.status())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Model = declarative_base()
