from pydantic import BaseModel

class Configuration(BaseModel):
    name: str
    value: dict


class ConfigurationUpdate(BaseModel):
    id: int
    name: str
    value: dict