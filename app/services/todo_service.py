from app.models.todo import Todo
from app.repositories.todo_repository import TodoRepository

class TodoService:
    def __init__(self, repository: TodoRepository):
        self.repository = repository

    def create_todo(self, user_email: str, title: str, description: str) -> Todo:
        return self.repository.create(user_email, title, description)

    def update_todo(self, user_email: str, todo_id: int, title: str, description: str) -> Todo | None:
        return self.repository.update(user_email, todo_id, title, description)

    def delete_todo(self, user_email: str, todo_id: int) -> bool:
        return self.repository.delete(user_email, todo_id)

    def download_todos(self, user_email: str, page: int, limit: int) -> tuple[list[Todo], int]:
        return self.repository.list_page(user_email, page, limit)