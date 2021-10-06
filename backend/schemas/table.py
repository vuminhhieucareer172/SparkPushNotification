from typing import List

from pydantic import BaseModel
from enum import Enum


class PrimaryKey(BaseModel):
    name_field: str = 'id'
    type: str
    auto_increment: bool = True


class OtherField(BaseModel):
    name_field: str
    type: str
    nullable: bool = True
    unique: bool = False
    default: str


class Engine(str, Enum):
    MYISAM = 'MyISAM'
    MEMORY = 'Memory'
    INNODB = 'InnoDB'
    ARCHIVE = 'Archive'
    NDB = 'NDB'


class FIElDS(BaseModel):
    primary: PrimaryKey
    others: List[OtherField]


class Table(BaseModel):
    name: str
    fields: FIElDS
    character_set: str = 'utf8'
    collate: str = 'utf8_general_ci'
    engine: Engine
