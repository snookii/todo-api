import uuid
from fastapi import APIRouter, HTTPException, status

from app.models.auth import RegisterRequest, LoginRequest, TokenResponse
from app.storage import users, tokens

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
def register(user: RegisterRequest):
    if user.email not in users:
        users[user.email] = user
        token = str(uuid.uuid4())
        tokens[token] = user.email
        return TokenResponse(token=token)

    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already registered")


@auth_router.post("/login", response_model=TokenResponse)
def login(user: LoginRequest):
    if user.email not in users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    else:
        saved_user = users[user.email]
        if saved_user.password == user.password:
            token = str(uuid.uuid4())
            tokens[token] = user.email
            return TokenResponse(token=token)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
