from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.constants import constants

# db mysql
engine = create_engine(
    constants.SQLALCHEMY_DATABASE_URI, **constants.SQLALCHEMY_ENGINE_OPTIONS
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = engine.connect()
