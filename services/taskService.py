from ..models.models import Task


class TaskService:
    store: dict[int, Task] = {}
    count = 1

    def add_task(self, name: str) -> Task:
        new_task = Task(id=self.count, name=name, status="todo")
        self.store[self.count] = new_task
        self.count += 1
        return new_task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.store.get(task_id)

    def get_tasks(self) -> list[Task]:
        return list(self.store.values())

    def delete_task(self, task_id) -> bool:
        if task_id in self.store:
            del self.store[task_id]
            self.count -= 1
            return True

        return False

    def update_task(self, id: int, name: str, status: str) -> tuple[bool, Task]:
        task_exists = True
        updated_task = Task(id=id, name=name, status=status)

        if id not in self.store:
            self.count += 1
            task_exists = False

        self.store[id] = updated_task
        return (task_exists, updated_task)
