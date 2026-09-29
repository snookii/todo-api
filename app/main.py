from fastapi import FastAPI

from app.routers.auth import auth_router
from app.routers.todos import todos_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(todos_router)