from fastapi import FastAPI
from .Routers import *


api = FastAPI()

api.include_router(Token)
api.include_router(Listener)
api.include_router(Collector)
api.include_router(Users)
