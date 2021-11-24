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


class ConfigEmail(BaseModel):
    host: str
    port: int
    email: str
    username: str
    password: str


class ConfigTelegram(BaseModel):
    token: str
