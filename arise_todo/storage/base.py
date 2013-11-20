import re
import uuid

from arise_todo.core.parser import Task


class BaseStorage(object):
    uuid_re = re.compile(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')

    def __init__(self):
        self._connected = False

    def _is_uuid(self, task):
        if isinstance(task, (str, unicode)):
            return self.uuid_re.match(task)
        elif isinstance(task, uuid.UUID):
            return True
        return False

    def _fake_task(self, task_uuid):
        return Task('', task_id=task_uuid)

    def task(self, task):
        if isinstance(task, Task):
            return task
        elif self._is_uuid(task):
            return self._fake_task(task)
        elif isinstance(task, (str, unicode)):
            return Task(task)
        raise TypeError

    def get(self, task_uuid):
        raise NotImplementedError

    def add(self, task, after_task=None, before_task=None):
        raise NotImplementedError

    def delete(self, task_or_uuid):
        raise NotImplementedError

    def replace(self, task_or_uuid, new_task):
        raise NotImplementedError

    def move_after(self, task_or_uuid, after_task_or_uuid):
        """
        Places the task after `after_task`
        """
        raise NotImplementedError

    def move_before(self, task_or_uuid, before_task_or_uuid):
        """
        Places the task before `before_task`
        """
        raise NotImplementedError

    def search(self, query, treat_as_regex=True):
        """
        Matches tasks with query
        """
        raise NotImplementedError

    def iterate(self):
        """
        Iterates over all tasks
        """
        raise NotImplementedError

    def __iter__(self):
        return iter(self.iterate())

    def __contains__(self, task):
        raise NotImplementedError

    def connect(self):
        self._connected = True

    def disconnect(self):
        self._connected = False

    @property
    def connected(self):
        return self._connected
