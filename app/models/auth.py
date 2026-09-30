from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=6, max_length=100)


class LoginRequest(BaseModel):
    email: str = Field(min_length=3, max_length=100)
    password: str = Field(min_length=1, max_length=100)


class TokenResponse(BaseModel):
    token: str