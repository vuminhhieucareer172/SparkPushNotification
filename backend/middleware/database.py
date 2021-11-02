from fastapi import HTTPException, status

from database.db import get_db


async def verify_database():
    db = get_db()
    if db is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fail to connect database")
    return db
