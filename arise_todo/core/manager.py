from .parser import Task
from .utils import get_storage


class TasksManager(object):

    def __init__(self, storage=None):
        self.storage = storage
        if self.storage is None:
            self.storage = get_storage()

    def _prepare_task(self, task_text):
        if isinstance(task_text, Task):
            return task_text
        return Task(task_text)

    def add(self, task):
        self.storage.add(self._prepare_task(task_text=task))

    def delete(self, task):
        self.storage.delete(self._prepare_task(task_text=task))

    def edit(self, task, new_task):
        self.storage.replace(self._prepare_task(task_text=task),
                             self._prepare_task(task_text=new_task))
