from fastapi import Depends, HTTPException, APIRouter
from ...Dependencies import get_current_user, get_user
from passlib.context import CryptContext
from .responses import *
import FastApi
import config

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/list")
async def read_users_all():
    response = [{'username': config.AppDatabase[x]['username'], 'superuser': config.AppDatabase[x]['superuser']} for x
                in config.AppDatabase]
    raise HTTPException(status_code=200, detail=response)


@router.get("/add")
async def add_user(username: str, password: str, repeat_password: str, current_user: User = Depends(get_current_user)):
    if not current_user.superuser:
        raise HTTPException(status_code=400, detail="You do not have enough rights")

    if not password == repeat_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if get_user(config.AppDatabase, username):
        raise HTTPException(status_code=400, detail="The user already exists")

    password_hash = get_password_hash(password)
    config.AppDatabase[username] = {'username': username, 'hashed_password': password_hash, 'superuser': 'false'}
    FastApi.DataBase.saveDB(True)
    raise HTTPException(status_code=200, detail="Success")


@router.get("/delete")
async def delete_user(username: str, current_user: User = Depends(get_current_user)):
    if not current_user.superuser:
        raise HTTPException(status_code=400, detail="You do not have enough rights")

    if not config.AppDatabase.pop(username, None):
        raise HTTPException(status_code=400, detail="This user does not exist")
    FastApi.DataBase.saveDB(True)
    raise HTTPException(status_code=200, detail="Success")


@router.get("/password")
async def change_password(new_password: str, second_new_password: str,username='', current_user: User = Depends(get_current_user)):
    user = current_user.username
    errors = []
    if username:
        if not current_user.superuser:
            raise HTTPException(status_code=400, detail="You do not have enough rights")
        user = username

        if not get_user(config.AppDatabase, user):
            errors.append("This user does not exist")

    if new_password != second_new_password:
        errors.append("Passwords do not match")

    if errors:
        raise HTTPException(status_code=400, detail=" and ".join(errors))

    password_hash = get_password_hash(new_password)
    config.AppDatabase[user]['hashed_password'] = password_hash
    FastApi.DataBase.saveDB(True)
    raise HTTPException(status_code=200, detail="Success")


def get_password_hash(password):
    return pwd_context.hash(password)
