from typing import List

from pydantic import BaseModel
from enum import Enum


class FieldSQL(BaseModel):
    name_field: str
    collation: str = 'latin1_swedish_ci'
    type: str
    comment: str = None


class PrimaryKey(FieldSQL):
    name_field = 'id'
    auto_increment: bool = True


class OtherField(FieldSQL):
    nullable: bool = True
    unique: bool = False
    default: str = None
    length: int = None
    value: str = None


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
    charset: str = 'latin1'
    collate: str = 'latin1_swedish_ci'
    engine: Engine = 'InnoDB'
