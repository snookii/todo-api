from pydantic import BaseModel


class TodoCreateRequest(BaseModel):
    title: str
    description: str

class TodoUpdateRequest(BaseModel):
    title: str
    description: str

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str

class TodoListResponse(BaseModel):
    data: list[TodoResponse]
    page: int
    limit: int
    total: int