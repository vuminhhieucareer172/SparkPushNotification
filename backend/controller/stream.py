from fastapi import status
from sqlalchemy import exc
from starlette.responses import JSONResponse

from backend.controller.table import create_table_streaming
from backend.schemas.stream import Stream
from backend.models.dbstreaming_kafka_streaming import KafkaStreaming
from database import session


def add_stream(new_schema: Stream):
    is_create_table_success = create_table_streaming(new_schema.table)
    if is_create_table_success.status_code != status.HTTP_201_CREATED:
        return is_create_table_success

    try:
        session.add(KafkaStreaming.from_json(new_schema.table.name, new_schema.topic_kafka_input))
        session.commit()
    except exc.SQLAlchemyError as e:
        print(e)
        session.rollback()
        return JSONResponse(content={"message": "Failed"},
                            status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse({"message": "Successful"}, status_code=status.HTTP_201_CREATED)
