import os
import operator
from funcy import ikeep, any, partial, ifilter, first, imap, select

from arise_todo.core.parser import Task
from ..base import BaseStorage


class TextStorage(BaseStorage):
    def __init__(self, file_name, keep_opened=False):
        super(TextStorage, self).__init__()
        self._keep_opened = keep_opened
        self._file_name = os.path.realpath(os.path.expanduser(file_name))
        self._fd = None

    @property
    def _file(self):
        if not self._keep_opened or self._fd is None or (self._fd and self._fd.closed):
            if self._fd and not self._fd.closed:
                self._fd.close()
            self._fd = open(self._file_name, 'a+')
        return self._fd

    def _atomic_write(self, tasks):
        tasks = map(u'{!s}\n'.format, tasks)
        self._file.truncate()
        self._file.writelines(tasks)
        self._file.flush()

    def __contains__(self, task):
        return any(partial(operator.eq, task), self)

    def get(self, task_uuid):
        return first(ifilter(partial(operator.eq, self.task(task_uuid)), self))

    def add(self, task, after_task=None, before_task=None):
        if task not in self:
            self._file.write('{!s}\n'.format(task))
            self._file.flush()

    def delete(self, task):
        tasks = ifilter(partial(operator.ne, self.task(task)), self)
        self._atomic_write(tasks)

    def replace(self, task_or_uuid, new_task):
        src_task = self.task(task_or_uuid)
        tasks = imap(lambda t: self.task(new_task) if t == src_task else t, self)
        self._atomic_write(tasks)

    def search(self, query, treat_as_regex=True):
        if treat_as_regex:
            return map(Task, select(query, self.iterate(raw=True)))
        return map(Task, ifilter(lambda t: query in t, self.iterate(raw=True)))

    def move_before(self, task_or_uuid, before_task_or_uuid, shift=0):
        task, before = self.task(task_or_uuid), self.task(before_task_or_uuid)
        tasks = list(self)
        if task in tasks:
            tasks.remove(task)
            tasks.insert(tasks.index(before) + shift if before in tasks else len(tasks), task)
            self._atomic_write(tasks)

    def move_after(self, task_or_uuid, after_task_or_uuid):
        self.move_before(task_or_uuid, after_task_or_uuid, shift=1)

    def iterate(self, raw=False):
        if raw:
            return ikeep(self._file)
        return ikeep(Task, self._file)
