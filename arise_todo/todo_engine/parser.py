from inspect import isclass
import operator
import re
from funcy import any_fn

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
        self.data = self._parse(src_text)

    def _parse(self, src_text):
        if self.pattern:
            match = self.pattern.search(src_text)
            return match.group(1) if match else self.EMPTY
        return src_text

    def _format(self, item):
        return item

    def format(self):
        if self.data:
            return self._format(self.data)
        return self.EMPTY

    def clean(self, src_text):
        """Removes itself from src_text"""
        return src_text.replace(self.format(), '')

    @property
    def name(self):
        return re.sub(r'([A-Z])', '_\1', self.__class__.__name__.replace('Item', ''))

    __str__ = __unicode__ = format


class MultipleTaskItem(TaskItem):
    def _parse(self, src_text):
        return self.pattern.findall(src_text)

    def _format(self, projects):
        return ' '.join('{!s}'.format(prj) for prj in projects)

    def clean(self, src_text):
        for prj in self.format().split():
            src_text = src_text.replace(prj, '')
        return src_text


class PriorityItem(TaskItem):
    pattern = re.compile(r'\(([A-Z]\d*)\)')

    def _format(self, data):
        return '({})'.format(data)


class CreationDateItem(TaskItem):
    pattern = re.compile(r'^({})'.format(DATE_TIME_RE))


class SchedulingItem(TaskItem):
    pattern = re.compile(r'#({})'.format(DATE_TIME_RE))

    def _format(self, data):
        return '#{}'.format(data)


class FadingDateItem(TaskItem):
    pattern = re.compile(r'#~({})'.format(DATE_TIME_RE))

    def _format(self, data):
        return '#~{}'.format(data)


class TaskMsgItem(TaskItem):
    @property
    def data(self):
        return self.task.clean_text

    @data.setter
    def data(self, value):
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
    STATES = ('todo', 'in-progress', 'done', 'removed', 'skipped')
    UNKNOWN_STATE = 'unknown'

    def _parse(self, src_text):
        value = super(StateItem, self)._parse(src_text)
        return value if not value or any(map(value.lower().startswith, self.STATES)) else self.UNKNOWN_STATE

    def _format(self, item):
        return '&{}'.format(item)


class MetadataItem(MultipleTaskItem):
    pattern = re.compile(r'''([\w-]+:([\w-]+|"[^"]+"|'[^']+'))''')

    def _parse(self, src_text):
        return [match[0] for match in self.pattern.findall(src_text)]


class Task(object):
    """
    Handling data
    + priority (A)
    + projects +prj +prj1
    + contexts @ctx @ctx1
    + scheduling #2013-09-25
    + state &done(2013-09-10 22:10)
    + creation date
    + task msg
    + metadata key:value pairs in the task msg
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
        MetadataItem,
    ]

    def __init__(self, todo_text):
        self.src_text = todo_text
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

    @property
    def data(self):
        return {p.name: p.data for p in self.task_parts}

    def __str__(self):
        return ' '.join(filter(operator.truth, map(operator.methodcaller('format'), self.task_parts)))