from sqlalchemy import Engine, text
from app.models.todo import Todo

class TodoRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def find_one(self, user_email: str, todo_id: int) -> Todo | None:
        with self.engine.connect() as connection:
            row = connection.execute(
                text("""
                    SELECT id, title, description FROM todos
                    WHERE user_email = :email AND id = :id
                """),
                {"email": user_email, "id": todo_id},
            ).fetchone()
        if row is None:
            return None
        return Todo(
            id=row.id,
            title=row.title,
            description=row.description,
        )

    def create(self, user_email: str, title: str,
               description: str) -> Todo:
        with self.engine.begin() as connection:
            result = connection.execute(
                text("""
                INSERT INTO todos (user_email, title, description) 
                VALUES (:email, :title, :description)
                """),
                {"email": user_email, "title": title, "description": description}
            )
            new_id = result.lastrowid
        return Todo(
            id=new_id,
            title=title,
            description=description,
        )

    def update(self, user_email: str, todo_id: int,
               title: str, description: str) -> Todo | None:
        with self.engine.begin() as connection:
            result = connection.execute(
                text("""
                UPDATE todos 
                SET title = :title, description = :description 
                WHERE id = :id AND user_email = :email
                     """),
                {"title": title, "description": description, "id": todo_id, "email": user_email}
            )
            changed = result.rowcount
        if changed == 0:
            return None
        return Todo(
            id=todo_id,
            title=title,
            description=description,
        )

    def delete(self, user_email: str, todo_id: int) -> bool:
        with self.engine.begin() as connection:
            result = connection.execute(
                text("""
                DELETE FROM todos 
                WHERE id = :id AND user_email = :email
                """),
                {"id": todo_id, "email": user_email}
            )
            deleted = result.rowcount
        if deleted == 0:
            return False
        else:
            return True

    def list_page(self, user_email: str, page: int,
                  limit: int) -> tuple[list[Todo], int]:
        offset = (page - 1) * limit
        with self.engine.connect() as connection:
            result =  connection.execute(
                text("""
                    SELECT id, title, description FROM todos
                    WHERE user_email = :email
                    ORDER BY id
                    LIMIT :limit OFFSET :offset
                """),
                {"offset": offset, "email": user_email, "limit": limit}
            )
            rows = result.all()
            todos = []
            for row in rows:
                todos.append(Todo(id=row.id, title=row.title, description=row.description))
            count_row = connection.execute(
                text("SELECT COUNT(*) AS total FROM todos "
                     "WHERE user_email = :email"),
                {"email": user_email}
            ).one()
            total = count_row.total
        return todos, total
