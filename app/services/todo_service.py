class TodoService:
    def __init__(self):
        self.tasks = {}
        self.next_ids = {}

    def create_todo(self, user_email: str, request):
        if user_email not in self.next_ids:
            self.next_ids[user_email] = 1
        if user_email not in self.tasks:
            self.tasks[user_email] = {}

        task_id = self.next_ids[user_email]
        self.tasks[user_email][task_id] = {
            "id": task_id,
            "title": request.title,
            "description": request.description
        }
        self.next_ids[user_email] += 1
        return self.tasks[user_email][task_id]

    def update_todo(self, user_email: str, todo_id: int, request):
        if user_email not in self.tasks:
            return None
        if todo_id not in self.tasks[user_email]:
            return None

        self.tasks[user_email][todo_id]["title"] = request.title
        self.tasks[user_email][todo_id]["description"] = request.description
        return self.tasks[user_email][todo_id]

    def delete_todo(self, user_email: str, todo_id: int):
        if user_email not in self.tasks:
            return False
        if todo_id not in self.tasks[user_email]:
            return False

        del self.tasks[user_email][todo_id]
        return True

    def download_todos(self, user_email: str, page: int, limit: int):
        if user_email not in self.tasks:
            return [], 0

        all_tasks = list(self.tasks[user_email].values())
        start = (page - 1) * limit
        end = start + limit
        return all_tasks[start:end], len(all_tasks)