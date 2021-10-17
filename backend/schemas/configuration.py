from pydantic import BaseModel

class Configuration(BaseModel):
    name: str
    value: str