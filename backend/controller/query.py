from sqlalchemy import exc
from starlette.responses import JSONResponse
from starlette import status
from backend.models.dbstreaming_query import UserQuery
from backend.schemas.query import Query, QueryUpdate
from database import session


def add_query(new_query: Query):
    query = UserQuery.from_json(new_query)
    try:
        session.add(query)
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": e}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def update_query(new_query: QueryUpdate):
    query = session.query(UserQuery).filter_by(username=new_query.id).scalar()
    try:
        query.sql = new_query.sql
        query.topic_kafka_output = new_query.topic_kafka_output
        query.contact = new_query.contact
        query.time_trigger = new_query.time_trigger
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": e}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)


def delete_query(query_id: int):
    try:
        session.query(UserQuery).filter_by(id=query_id).delete()
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed", "detail": e}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)
