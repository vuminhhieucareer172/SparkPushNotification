import logging
import os
from urllib.parse import urlencode

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()


class DB:
    __instance = None

    def __init__(self):
        """ Virtually private constructor. """

        if DB.__instance is not None:
            raise Exception(
                "This class is a singleton, use DB.create()")
        else:
            DB.__instance = self
        self.engine = self.create_engine()

    @staticmethod
    def create():
        if DB.__instance is None:
            DB.__instance = DB()
        return DB.__instance

    @staticmethod
    def get_credentials():
        """ Fetch credentials from either environment variables (for testing)"""
        return dict(
            drivername=os.getenv('DB_DRIVER'),
            username=os.getenv('DB_USERNAME', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'some_password'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME', 'user_database'),
            query={"charset": os.getenv('DB_CHARSET')}
        )

    def create_engine(self):
        credentials = self.get_credentials()

        return sqlalchemy.create_engine('{engine}://{user}:{password}@{host}:{port}/{database}?{query}'.format(
            engine=credentials['drivername'],
            user=credentials['username'],
            password=credentials['password'],
            host=credentials['host'],
            port=int(credentials['port']),
            database=credentials['database'],
            query=urlencode(credentials['query'])
        ),
            pool_size=200,
            max_overflow=0,
            echo=bool(os.getenv('DB_DEBUG', False))
        )

    def connect(self):
        return self.engine.connect()


db = DB.create()
engine = db.engine
meta = MetaData(engine)
logging.info("connected to database with config:", engine.pool.status())

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Model = declarative_base()
