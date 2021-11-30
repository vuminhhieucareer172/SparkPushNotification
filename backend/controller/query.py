from sqlalchemy import exc
from starlette import status
from starlette.responses import JSONResponse

from backend.controller.schedule import add_job_output, scheduler, update_job_output
from backend.models.dbstreaming_query import UserQuery
from backend.schemas.query import Query, QueryUpdate
from database.db import DB, get_session
from database.session import SessionHandler


def get_query(db: DB, skip: int = 0, limit: int = 10):
    session = get_session(database=db)
    try:
        query_session = SessionHandler.create(session, UserQuery)
        return JSONResponse(query_session.get_from_offset(skip, limit, to_json=True), status_code=status.HTTP_200_OK)
    except exc.SQLAlchemyError as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def get_query_by_id(id_query: int, db: DB):
    session = get_session(database=db)
    try:
        query_session = SessionHandler.create(session, UserQuery)
        return JSONResponse(query_session.get_one(query_dict=dict(id=id_query), to_json=True),
                            status_code=status.HTTP_200_OK)
    except exc.SQLAlchemyError as e:
        print(e)
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def add_query(new_query: Query, db: DB):
    session = get_session(database=db)
    try:
        query_session = SessionHandler.create(session, UserQuery)
        query_session.add(new_query.dict())
        session.commit()
        result_add_job = add_job_output(UserQuery(topic_kafka_output=new_query.topic_kafka_output,
                                                  time_trigger=new_query.time_trigger,
                                                  contact=new_query.contact))
        # result_add_job = 'ok'
        if result_add_job == "ok":
            return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)
        return JSONResponse(content={"message": result_add_job}, status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def update_query(new_query: QueryUpdate, db: DB):
    session = get_session(database=db)
    try:
        query_session = SessionHandler.create(session, UserQuery)
        query = query_session.get(_id=new_query.id)
        if query is None:
            return JSONResponse(content={"message": "Not found query"}, status_code=status.HTTP_404_NOT_FOUND)
        query.sql = new_query.sql
        query.topic_kafka_output = new_query.topic_kafka_output
        query.contact = new_query.contact
        query.time_trigger = new_query.time_trigger
        session.commit()
        result_update = update_job_output(new_query=query)
        if result_update == "ok":
            return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)
        return JSONResponse(content={"message": result_update}, status_code=status.HTTP_400_BAD_REQUEST)
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)


def delete_query(query_id: int, db: DB):
    session = get_session(database=db)
    try:
        query_session = SessionHandler.create(session, UserQuery)
        query_in_db: UserQuery = query_session.get(_id=query_id)
        query_session.delete(dict(id=query_id))
        session.commit()
        scheduler.remove_job(job_id=query_in_db.topic_kafka_output)
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Error: {}".format(str(e))}, status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_200_OK)
