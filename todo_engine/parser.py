from inspect import isclass
import operator
import re

FILE = 'todo.txt'

DATE_YYYY = r'(\d{4})'
DATE_MM = r'(10|11|12|(0?\d))'
DATE_DD = r'([012]?\d|30|31)'
DATE_RE = r'({yyyy}(-{mm})?(-{dd})?)'.format(yyyy=DATE_YYYY, mm=DATE_MM, dd=DATE_DD)

TIME_HH = r'([01]?\d|2[0-4])'
TIME_MM = r'([0-5]?\d)'
TIME_SS = r'({mm}|60|61)'.format(mm=TIME_MM)
TIME_RE = r'({hh}:{mm}(:{ss})?)'.format(hh=TIME_HH, mm=TIME_MM, ss=TIME_SS)

DATE_TIME_RE = r'({date}( {time})?)'.format(date=DATE_RE, time=TIME_RE)


class TaskItem(object):
    pattern = None
    EMPTY = ''

    def __init__(self, src_text, task):
        self.task = task
        self.item = self._parse(src_text)

    def _parse(self, src_text):
        if self.pattern:
            match = self.pattern.search(src_text)
            return match.group(1) if match else self.EMPTY
        return src_text

    def _format(self, item):
        return item

    def format(self):
        if self.item:
            return self._format(self.item)
        return self.EMPTY

    def clean(self, src_text):
        """Removes itself from src_text"""
        return src_text.replace(self.format(), '')

    __str__ = __unicode__ = format


class MultipleTaskItem(TaskItem):
    def _parse(self, src_text):
        return self.pattern.findall(src_text)

    def clean(self, src_text):
        for prj in self.format().split():
            src_text = src_text.replace(prj, '')
        return src_text


class PriorityItem(TaskItem):
    pattern = re.compile(r'\(([A-Z]\d*)\)')

    def _format(self, item):
        return '({})'.format(self.item)


class CreationDateItem(TaskItem):
    pattern = re.compile(r'^({})'.format(DATE_TIME_RE))


class SchedulingItem(TaskItem):
    pattern = re.compile(r'#({})'.format(DATE_TIME_RE))

    def _format(self, item):
        return '#{}'.format(item)


class FadingDateItem(TaskItem):
    pattern = re.compile(r'#~({})'.format(DATE_TIME_RE))

    def _format(self, item):
        return '#~{}'.format(item)


class TaskMsgItem(TaskItem):
    @property
    def item(self):
        return self.task.clean_text

    @item.setter
    def item(self, value):
        pass


class ProjectsItem(MultipleTaskItem):
    pattern = re.compile(r'\+([\w/-]+)')

    def _format(self, projects):
        return ' '.join('+{}'.format(prj) for prj in projects)


class ContextsItem(MultipleTaskItem):
    pattern = re.compile(r'@([\w/-]+)')

    def _format(self, projects):
        return ' '.join('@{}'.format(prj) for prj in projects)


class StateItem(TaskItem):
    pattern = re.compile(r'&([\w-]+(\({datetime}\))?)'.format(datetime=DATE_TIME_RE))

    def _format(self, item):
        return '&{}'.format(item)


class Task(object):
    """
    Handling data
    + priority (A)
    + projects +prj +prj1
    + contexts @ctx @ctx1
    - scheduling #2013-09-25
    - state &done(2013-09-10 22:10)
    - creation date
    + task msg
    - metadata key:value pairs in the task msg
    - mentioned people <miph>
    """
    TASK_PARTS = [
        CreationDateItem,
        PriorityItem,
        StateItem,
        TaskMsgItem,
        ProjectsItem,
        ContextsItem,
        FadingDateItem,
        SchedulingItem,
    ]

    STATES = ('todo', 'in-progress', 'done', 'removed')

    def __init__(self, todo_text):
        self.clean_text = ''
        self.task_parts = []
        for part in self.TASK_PARTS:
            if isclass(part) and issubclass(part, TaskItem) or callable(part):
                self.task_parts.append(part(todo_text, self))
            else:
                self.task_parts.append(part)

        cleaned_text = todo_text
        for part in self.task_parts:
            if isinstance(part, TaskItem):
                cleaned_text = part.clean(cleaned_text)
        self.clean_text = re.sub(r'\s{2,}', ' ', cleaned_text).strip()

    def __str__(self):
        return ' '.join(filter(operator.truth, map(operator.methodcaller('format'), self.task_parts)))


if __name__ == '__main__':
    print Task('(A) task')
    print Task('task (A)')
    print Task('task (A12)   ksat')
    print Task('(A) task +prj')
    print Task('(A) task +prj-prj')
    print Task('(A) task +prj/prj +jrp')
    print Task(' +prj (A) task')
    print Task('(A) +prj-prj task ')
    print Task('+prj/prj (A) task  +jrp')
    print Task('(A) task +prj @ctx')
    print Task('(A) task +prj-prj @ctx-ctx')
    print Task('(A) task +prj/prj +jrp @ctx/ctx @xtc')
    print Task(' +prj @ctx (A) task')
    print Task('(A) +prj-prj @ctx-ctx task ')
    print Task('+prj/prj @ctx/ctx (A) task  +jrp @xtc')
    print Task('(A) task &todo')
    print Task('(A) task &in-progress')
    print Task('(A) task &done(2013-11-10 22:33)')
    print Task('(A) task #2013-11-10 22:33 task')
    print Task('(A) task #~2013-11-10 22:33 task')
    print Task('(A) task #2013-11-10 22:33 #~2013-11-10 23:33 task')
