class BaseStorage(object):

    def add(self, task, after_task=None, before_task=None):
        raise NotImplementedError

    def delete(self, task):
        raise NotImplementedError

    def replace(self, task):
        raise NotImplementedError

    def move_after(self, task, after_task):
        """
        Places the task after `after_task`
        """
        raise NotImplementedError

    def move_before(self, task, before_task):
        """
        Places the task before `before_task`
        """
        raise NotImplementedError

    def search(self, query):
        """
        Matches tasks with query
        """
        raise NotImplementedError

    def iterate(self):
        """
        Iterates over all tasks
        """
        raise NotImplementedError
