import random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse

app = FastAPI()

class User(BaseModel):
    name: str
    email: str
    password: str

class Todo(BaseModel):
    title: str
    description: str
    token: float

users = {}
tokens = {}
tasks = {}
next_ids = {}

@app.post("/register")
def register(user: User):
    if user.email not in users:
        users[user.email] = user
        token = random.random()
        tokens[token] = user.email
        return {"token": token}

    return {"error": "jest juz zarejestrowany"}

@app.post("/login")
def login(user: User):
    if user.email not in users:
        return {"error": "email nie jest zarejestrowany"}
    else:
        saved_user = users[user.email]
        if saved_user.password == user.password:
            token = random.random()
            tokens[token] = user.email
            return {"token": token}
        else:
            return {"error": "błędne hasło"}

@app.post("/todos")
def create_todo(todo: Todo):
    if todo.token not in tokens:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    emails = tokens[todo.token]

    if emails not in next_ids:
        next_ids[emails] = 1

    if emails not in tasks:
        tasks[emails] = {}

    task_id = next_ids[emails]
    tasks[emails][task_id] = {
        "id": task_id,
        "title": todo.title,
        "description": todo.description
    }
    next_ids[emails] += 1
    return {
        "id": task_id,
        "title": todo.title,
        "description": todo.description
    }

@app.put("/todos/{todo_id}")
def update_task(todo_id: int, todo: Todo):
    if todo.token not in tokens:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    emails = tokens[todo.token]

    if emails not in tasks:
        return JSONResponse(status_code=404, content={"message": "Nie ma tylu zadań"})
    if todo_id not in tasks[emails]:
        return JSONResponse(status_code=404, content={"message": "Nie ma tylu zadań"})

    tasks[emails][todo_id]["title"] = todo.title
    tasks[emails][todo_id]["description"] = todo.description
    return {
        "id": todo_id,
        "title": todo.title,
        "description": todo.description
    }

@app.delete("/todos/{todo_id}")
def delete_task(todo_id: int, todo: Todo):
    if todo.token not in tokens:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    emails = tokens[todo.token]

    if emails not in tasks:
        return JSONResponse(status_code=404, content={"message": "Nie ma tylu zadań"})
    if todo_id not in tasks[emails]:
        return JSONResponse(status_code=404, content={"message": "Nie ma tylu zadań"})

    del tasks[emails][todo_id]
    return JSONResponse(status_code=204, content=None)

@app.get("/todos")
def download_todos (token: float, page: int = 1, limit: int = 10):
    if token not in tokens:
        return JSONResponse(status_code=401, content={"message": "Unauthorized"})

    emails = tokens[token]

    if emails not in tasks:
        return {
            "data": [],
            "page": page,
            "limit": limit,
            "total": 0
        }

    user_tasks = tasks[emails]
    all_tasks = list(user_tasks.values())
    start = (page - 1) * limit
    end = start + limit
    return {
        "data": all_tasks[start:end],
        "page": page,
        "limit": limit,
        "total": len(all_tasks),
    }
