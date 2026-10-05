from pydantic import BaseModel, Field


class TodoCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)

class TodoUpdateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=1000)

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str

class Todo(BaseModel):
    id: int
    title: str
    description: str

class TodoListResponse(BaseModel):
    data: list[TodoResponse]
    page: int
    limit: int
    total: int