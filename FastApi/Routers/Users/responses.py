from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    username: str
    superuser: Union[bool, None] = None
