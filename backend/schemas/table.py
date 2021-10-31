from typing import List

from pydantic import BaseModel
from enum import Enum


class Field(BaseModel):
    name_field: str
    type: str
    length: int = None
    value: str = None
    primary_key: bool = False
    nullable: bool = True
    unique: bool = False
    default: str = None
    auto_increment: bool = False
    collation: str = 'latin1_swedish_ci'
    comment: str = None


class Engine(str, Enum):
    MYISAM = 'MyISAM'
    MEMORY = 'Memory'
    INNODB = 'InnoDB'
    ARCHIVE = 'Archive'
    NDB = 'NDB'


class Table(BaseModel):
    name: str
    fields: List[Field]
    collate: str = 'latin1_swedish_ci'
    engine: Engine = 'InnoDB'
