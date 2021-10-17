import logging

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from constants import constants
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONNECT = dict(
    drivername=os.getenv('DB_DRIVER'),
    username=os.getenv('DB_USERNAME'),
    password=os.getenv('DB_PASSWORD'),
    host=os.getenv('DB_HOST'),
    port=os.getenv('DB_PORT'),
    database=os.getenv('DB_NAME'),
    query={"charset": os.getenv('DB_CHARSET')}
)

engine = create_engine(
    URL(**DB_CONNECT), **constants.SQLALCHEMY_ENGINE_OPTIONS
)
meta = MetaData(engine)
db = engine.connect()
logging.info("connected to database with config:", engine.pool.status())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Model = declarative_base()
