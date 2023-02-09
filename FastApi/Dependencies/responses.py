from typing import Union
from pydantic import BaseModel


class TokenData(BaseModel):
    username: Union[str, None] = None


class User(BaseModel):
    username: str
    superuser: Union[bool, None] = None


class UserInDB(User):
    hashed_password: str
