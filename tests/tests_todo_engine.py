from unittest import TestCase

from hamcrest import *
from arise_todo.todo_engine.parser import Task


class TaskTest(TestCase):
    
    TEST_DATA = (
        ('(A) task', '(A) task'),
        ('task (A)', '(A) task'),
        ('task (A12)   ksat', '(A12) task ksat'),
        ('(A) task +prj', '(A) task +prj'),
        ('(A) task +prj-prj', '(A) task +prj-prj'),
        ('(A) task +prj/prj +jrp', '(A) task +prj/prj +jrp'),
        (' +prj (A) task', '(A) task +prj'),
        ('(A) +prj-prj task ', '(A) task +prj-prj'),
        ('+prj/prj (A) task  +jrp', '(A) task +prj/prj +jrp'),
        ('(A) task +prj @ctx', '(A) task +prj @ctx'),
        ('(A) task +prj-prj @ctx-ctx', '(A) task +prj-prj @ctx-ctx'),
        ('(A) task +prj/prj +jrp @ctx/ctx @xtc', '(A) task +prj/prj +jrp @ctx/ctx @xtc'),
        (' +prj @ctx (A) task', '(A) task +prj @ctx'),
        ('(A) +prj-prj @ctx-ctx task ', '(A) task +prj-prj @ctx-ctx'),
        ('+prj/prj @ctx/ctx (A) task  +jrp @xtc', '(A) task +prj/prj +jrp @ctx/ctx @xtc'),
        ('(A) task &todo', '(A) &todo task'),
        ('(A) task &in-progress', '(A) &in-progress task'),
        ('(A) task &done(2013-11-10 22:33)', '(A) &done(2013-11-10 22:33) task'),
        ('(A) task #2013-11-10 22:33 task', '(A) task task #2013-11-10'),
        ('(A) task #~2013-11-10 22:33 task', '(A) task task #~2013-11-10 22:33'),
        ('(A) task #2013-11-10 22:33 #~2013-11-10 23:33 task',
         '(A) task task #~2013-11-10 23:33 #2013-11-10 22:33 22:33 23:33'),
        ('(A) task key:value key1:"value value"', '(A) task key:value key1:"value value"'),
        ('(A) task key:value key1:"value value" task-continue asdf..',
         '(A) task task-continue asdf.. key:value key1:"value value"'),
    )
    
    def test_init(self):
        for task, expected in self.TEST_DATA:
            assert_that(unicode(Task(task)), equal_to(expected))

    def test_consistent(self):
        for task, expected in self.TEST_DATA:
            assert_that(unicode(Task(unicode(Task(task)))), equal_to(expected))

    def test_data(self):
        for task, expected in self.TEST_DATA:
            #print task, Task(task).data
            pass
