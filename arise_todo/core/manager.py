from .parser import Task
from .utils import get_storage


class TasksManager(object):

    def __init__(self, storage=None):
        self._storage = storage
        if self._storage is None:
            self._storage = get_storage()

    def close(self):
        if self._storage.connected:
            self._storage.disconnect()

    @property
    def storage(self):
        if not self._storage.connected:
            self._storage.connect()
        return self._storage

    def add(self, task):
        self.storage.add(self._storage.task(task))

    def delete(self, task):
        self.storage.delete(self._storage.task(task))

    def edit(self, task, new_task):
        self.storage.replace(self._storage.task(task),
                             self._storage.task(new_task))

    def search(self, query):
        return self.storage.search(query)

    def move_after(self, task, after):
        self.storage.move_after(task, after)

    def move_before(self, task, before):
        self.storage.move_after(task, before)

    def __iter__(self):
        return iter(self.storage)
