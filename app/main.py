from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.database import initialize_database
from app.routers.auth import auth_router
from app.routers.todos import todos_router
from app.middleware.authentication import authentication_middleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(auth_router)
app.include_router(todos_router)
app.middleware("http")(authentication_middleware)