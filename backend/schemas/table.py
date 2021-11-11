from typing import List, Optional

from pydantic import BaseModel
from enum import Enum


class Field(BaseModel):
    name_field: str
    type: str
    length: int = None
    value: str = None
    primary_key: bool = False
    not_null: bool = False
    unique: bool = False
    default: str = None
    auto_increment: bool = False
    collation: Optional[str] = 'latin1_swedish_ci'
    comment: Optional[str] = None


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
