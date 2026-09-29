from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

from app.models.todo import (
    TodoCreateRequest,
    TodoUpdateRequest,
    TodoDeleteRequest,
    TodoResponse,
    TodoListResponse,
)
from app.storage import tokens, tasks, next_ids

todos_router = APIRouter(prefix="/todos")


@todos_router.post("", response_model=TodoResponse)
def create_todo(request: TodoCreateRequest):
    if request.token not in tokens:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    emails = tokens[request.token]

    if emails not in next_ids:
        next_ids[emails] = 1

    if emails not in tasks:
        tasks[emails] = {}

    task_id = next_ids[emails]
    tasks[emails][task_id] = {
        "id": task_id,
        "title": request.title,
        "description": request.description
    }
    next_ids[emails] += 1
    return TodoResponse(
        id=task_id,
        title=request.title,
        description=request.description
    )


@todos_router.put("/{todo_id}", response_model=TodoResponse)
def update_task(todo_id: int, request: TodoUpdateRequest):
    if request.token not in tokens:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    emails = tokens[request.token]

    if emails not in tasks:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    if todo_id not in tasks[emails]:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    tasks[emails][todo_id]["title"] = request.title
    tasks[emails][todo_id]["description"] = request.description
    return TodoResponse(
        id=todo_id,
        title=request.title,
        description=request.description
    )


@todos_router.delete("/{todo_id}")
def delete_task(todo_id: int, request: TodoDeleteRequest):
    if request.token not in tokens:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    emails = tokens[request.token]

    if emails not in tasks:
        return JSONResponse(status_code=404, content={"error": "Task not found"})
    if todo_id not in tasks[emails]:
        return JSONResponse(status_code=404, content={"error": "Task not found"})

    del tasks[emails][todo_id]
    return Response(status_code=204)


@todos_router.get("", response_model=TodoListResponse)
def download_todos(token: str, page: int = 1, limit: int = 10):
    if token not in tokens:
        return JSONResponse(status_code=401, content={"error": "Unauthorized"})

    emails = tokens[token]

    if emails not in tasks:
        return TodoListResponse(data=[], page=page, limit=limit, total=0)

    all_tasks = list(tasks[emails].values())
    start = (page - 1) * limit
    end = start + limit
    return TodoListResponse(
        data=all_tasks[start:end],
        page=page,
        limit=limit,
        total=len(all_tasks)
    )