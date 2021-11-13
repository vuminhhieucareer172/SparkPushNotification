from pydantic import BaseModel


class Configuration(BaseModel):
    name: str
    value: dict

    class Config:
        orm_mode = True


class ConfigurationUpdate(BaseModel):
    id: int = 0
    name: str
    value: dict

    class Config:
        orm_mode = True

