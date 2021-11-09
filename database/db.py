import os
from urllib.parse import urlencode

import sqlalchemy
from dotenv import load_dotenv
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker


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

    def re_create_engine(self):
        self.engine = self.create_engine()

    @staticmethod
    def get_credentials():
        """ Fetch credentials from either environment variables (for testing)"""
        load_dotenv(override=True)
        return dict(
            drivername=os.getenv('DB_DRIVER'),
            username=os.getenv('DB_USERNAME', 'mysql'),
            password=os.getenv('DB_PASSWORD', 'some_password'),
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', 5432),
            database=os.getenv('DB_NAME', 'user_database'),
            query={"charset": os.getenv('DB_CHARSET')}
        )

    def create_engine(self):
        credentials = self.get_credentials()
        try:
            return sqlalchemy.create_engine('{engine}://{user}:{password}@{host}:{port}/{database}?{query}'.format(
                engine=credentials['drivername'],
                user=credentials['username'],
                password=credentials['password'],
                host=credentials['host'],
                port=int(credentials['port'], 0),
                database=credentials['database'],
                query=urlencode(credentials['query'])
            ),
                pool_size=200,
                max_overflow=0,
                echo=bool(os.getenv('DB_DEBUG', False))
            )
        except Exception as e:
            print(e)
            return None

    def connect(self):
        return self.engine.connect()

    def close(self):
        self.__instance.close()


def object_as_dict(obj):
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def get_db():
    db = DB.create()
    if db.engine is None:
        return None
    return db


def get_session(database: DB):
    try:
        engine = database.engine
        Session = sessionmaker(bind=engine)
        return Session()
    except Exception as e:
        print(e)
        return None
