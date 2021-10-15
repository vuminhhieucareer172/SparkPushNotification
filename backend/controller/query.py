from sqlalchemy import exc
from starlette.responses import JSONResponse
from starlette import status
from backend.models.dbstreaming_query import UserQuery
from backend.schemas.query import Query
from database import session


def add_query(new_query: Query):
    query = UserQuery.from_json(new_query)
    try:
        session.add(query)
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed"},
                            status_code=status.HTTP_400_BAD_REQUEST)

    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)
