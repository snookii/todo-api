import uuid
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.models.auth import RegisterRequest, LoginRequest, TokenResponse
from app.storage import users, tokens

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", response_model=TokenResponse)
def register(user: RegisterRequest):
    if user.email not in users:
        users[user.email] = user
        token = str(uuid.uuid4())
        tokens[token] = user.email
        return TokenResponse(token=token)

    return JSONResponse(status_code=409, content={"error": "User already registered"})


@auth_router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest):
    if user.email not in users:
        return JSONResponse(status_code=401, content={"error": "Email not registered"})
    else:
        saved_user = users[user.email]
        if saved_user.password == user.password:
            token = str(uuid.uuid4())
            tokens[token] = user.email
            return TokenResponse(token=token)
        else:
            return JSONResponse(status_code=401, content={"error": "Incorrect password"})