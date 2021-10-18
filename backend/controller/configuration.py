import time

from sqlalchemy import exc
from starlette.responses import JSONResponse
from starlette import status
from backend.models.dbstreaming_config import Config
from backend.schemas.configuration import Configuration, ConfigurationUpdate
from database import session


def add_config(new_config: Configuration):
    config_record = Config.from_json(new_config)
    try:
        session.add(config_record)
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": e},
                            status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def update_config(new_config: ConfigurationUpdate):
    config_record = session.query(Config).filter_by(id=new_config.id).scalar()
    try:
        config_record.name = new_config.name
        config_record.value = new_config.value
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": e},
                            status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def delete_config(config_id: int):
    try:
        session.query(Config).filter_by(id=config_id).delete()
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": e}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)
