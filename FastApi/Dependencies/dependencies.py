from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

import config
import secrets
from .responses import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(data_base, username: str):
    if username in data_base:
        user_dict = data_base[username]
        return UserInDB(**user_dict)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, secrets.accessSettings["secret_key"],
                             algorithms=[secrets.accessSettings["algorithm"]])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(config.AppDatabase, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
