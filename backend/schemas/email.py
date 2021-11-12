from pydantic import BaseModel


class AuthEmail(BaseModel):
    host: str
    port: int
    email: str
    username: str
    password: str
