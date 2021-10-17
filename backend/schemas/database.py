from pydantic import BaseModel


class Database(BaseModel):
    db_driver: str = 'mysql'
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str
