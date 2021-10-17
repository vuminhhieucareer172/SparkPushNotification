from sqlalchemy import exc
from starlette.responses import JSONResponse
from starlette import status
from backend.models.dbstreaming_config import Config
from backend.schemas.configuration import Configuration
from database import session


def add_config(new_config: Configuration):
    config_record = Config.from_json(new_config)
    try:
        session.add(config_record)
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed"},
                            status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)
