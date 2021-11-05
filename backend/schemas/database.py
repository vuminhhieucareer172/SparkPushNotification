from enum import Enum

from pydantic import BaseModel


class DB_DRIVER_MANAGER(str, Enum):
    POSTGRESQL = ''
    MYSQL = ''
    SQLSERVER_17 = 'ODBC+Driver+17+for+SQL+Server'
    SQLSERVER_16 = 'ODBC+Driver+16+for+SQL+Server'
    SQLSERVER_15 = 'ODBC+Driver+15+for+SQL+Server'
    SQLSERVER_14 = 'ODBC+Driver+14+for+SQL+Server'
    SQLSERVER_13 = 'ODBC+Driver+13+for+SQL+Server'


class Database(BaseModel):
    db_driver: str = 'mysql'
    db_host: str
    db_port: int
    db_name: str
    db_username: str
    db_password: str
    db_driver_manager: DB_DRIVER_MANAGER = DB_DRIVER_MANAGER.MYSQL
