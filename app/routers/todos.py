from fastapi import APIRouter, Response, Depends, Query, Request, HTTPException, status
from fastapi.security import APIKeyHeader
from app.models.todo import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    TodoListResponse,
)
from app.services.todo_service import TodoService

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
todos_router = APIRouter(prefix="/todos", dependencies=[Depends(api_key_header)])
todo_service = TodoService()

@todos_router.post("", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_todo(body: TodoCreateRequest, request: Request):
    email = request.state.user
    return todo_service.create_todo(
        user_email=email,
        title=body.title,
        description=body.description,
    )

@todos_router.put("/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, body: TodoUpdateRequest, request: Request):
    email = request.state.user
    todo = todo_service.update_todo(user_email=email, todo_id=todo_id, title=body.title, description=body.description)

    if todo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return todo

@todos_router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, request: Request):
    email = request.state.user
    deleted = todo_service.delete_todo(user_email=email, todo_id=todo_id)

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@todos_router.get("", response_model=TodoListResponse)
def download_todos(request: Request,
                   page: int = Query(default=1, ge=1),
                   limit: int = Query(default=10, ge=1, le=100)
                   ):
    email = request.state.user
    todos, total = todo_service.download_todos(user_email=email, page=page, limit=limit)

    responses = []
    for todo in todos:
        responses.append(TodoResponse(id=todo.id, title=todo.title , description=todo.description))

    return TodoListResponse(
        data= responses,
        page=page,
        limit=limit,
        total=total
    )
