import random
from fastapi import FastAPI, APIRouter, Response
from pydantic import BaseModel
from fastapi.responses import JSONResponse


app = FastAPI()
auth_router = APIRouter(prefix="/auth")
todos_router = APIRouter(prefix="/todos")

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    token: str

class TodoCreateRequest(BaseModel):
    title: str
    description: str
    token: str

class TodoResponse(BaseModel):
    id: int
    title: str
    description: str

class TodoListResponse(BaseModel):
    data: list[TodoResponse]
    page: int
    limit: int
    total: int

class TodoUpdateRequest(BaseModel):
    title: str
    description: str
    token: str

class TodoDeleteRequest(BaseModel):
    token: str

users = {}
tokens = {}
tasks = {}
next_ids = {}

@auth_router.post("/register", response_model=TokenResponse)
def register(user: RegisterRequest):
    if user.email not in users:
        users[user.email] = user
        token = str(random.random())
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
            token = str(random.random())
            tokens[token] = user.email
            return TokenResponse(token=token)
        else:
            return JSONResponse(status_code=401, content={"error": "Incorrect password"})

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
        id = task_id,
        title = request.title,
        description = request.description
    )

@todos_router.put("/{todo_id}", response_model=TodoResponse)
def update_task(todo_id: int, request: TodoUpdateRequest):
    if request.token not in tokens:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    emails = tokens[request.token]

    if emails not in tasks:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    if todo_id not in tasks[emails]:
        return JSONResponse(status_code=404, content={"message": "Task not found"})

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
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    emails = tokens[request.token]

    if emails not in tasks:
        return JSONResponse(status_code=404, content={"message": "Task not found"})
    if todo_id not in tasks[emails]:
        return JSONResponse(status_code=404, content={"message": "Task not found"})

    del tasks[emails][todo_id]
    return Response(status_code=204)

@todos_router.get("", response_model=TodoListResponse)
def download_todos (token: str, page: int = 1, limit: int = 10):
    if token not in tokens:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    emails = tokens[token]

    if emails not in tasks:
        return TodoListResponse(
            data = [],
            page = page,
            limit = limit,
            total = 0
        )

    user_tasks = tasks[emails]
    all_tasks = list(user_tasks.values())
    start = (page - 1) * limit
    end = start + limit
    return TodoListResponse(
            data = all_tasks[start:end],
            page = page,
            limit = limit,
            total = len(all_tasks)
        )

app.include_router(auth_router)
app.include_router(todos_router)
