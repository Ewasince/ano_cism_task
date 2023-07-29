from pydantic import BaseModel


class UserCreds(BaseModel):
    login: str
    password: str
