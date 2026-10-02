from fastapi import APIRouter, Response, Depends, Query, Request
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from app.models.todo import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoResponse,
    TodoListResponse,
)
from app.storage import tasks, next_ids

api_key_header = APIKeyHeader(name="Authorization", auto_error=False)
todos_router = APIRouter(prefix="/todos", dependencies=[Depends(api_key_header)])

@todos_router.post("", response_model=TodoResponse)
def create_todo(body: TodoCreateRequest, request: Request):

    email = request.state.user

    if email not in next_ids:
        next_ids[email] = 1

    if email not in tasks:
        tasks[email] = {}

    task_id = next_ids[email]
    tasks[email][task_id] = {
        "id": task_id,
        "title": body.title,
        "description": body.description
    }
    next_ids[email] += 1
    return TodoResponse(
        id=task_id,
        title=body.title,
        description=body.description
    )

@todos_router.put("/{todo_id}", response_model=TodoResponse)
def update_task(todo_id: int, body: TodoUpdateRequest, request: Request):

    email = request.state.user

    if email not in tasks:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    if todo_id not in tasks[email]:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    tasks[email][todo_id]["title"] = body.title
    tasks[email][todo_id]["description"] = body.description
    return TodoResponse(
        id=todo_id,
        title=body.title,
        description=body.description
    )

@todos_router.delete("/{todo_id}")
def delete_task(todo_id: int, request: Request):

    email = request.state.user

    if email not in tasks:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    if todo_id not in tasks[email]:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    del tasks[email][todo_id]
    return Response(status_code=204)


@todos_router.get("", response_model=TodoListResponse)
def download_todos(request: Request,
                   page: int = Query(default=1, ge=1),
                   limit: int = Query(default=10, ge=1, le=100)
                   ):

    email = request.state.user

    if email not in tasks:
        return TodoListResponse(data=[], page=page, limit=limit, total=0)

    all_tasks = list(tasks[email].values())
    start = (page - 1) * limit
    end = start + limit
    return TodoListResponse(
        data=all_tasks[start:end],
        page=page,
        limit=limit,
        total=len(all_tasks)
    )
