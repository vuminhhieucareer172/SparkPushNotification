from pydantic import BaseModel


class Configuration(BaseModel):
    name: str
    value: dict

    class Config:
        orm_mode = True


class ConfigurationUpdate(BaseModel):
    id: int
    name: str
    value: dict
<<<<<<< HEAD

    class Config:
        orm_mode = True
=======
>>>>>>> 3198386816c3273b0881d681b7526317bdedafda
