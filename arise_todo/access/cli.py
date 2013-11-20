from __future__ import unicode_literals
import cmd
from arise_todo.core.manager import TasksManager


class CLI(cmd.Cmd):
    intro = 'Simple tasks CLI'
    prompt = '> '

    def _print_tasks(self, tasks):
        for task in tasks:
            print '[{t.id!s}] {t!s}'.format(t=task)

    def emptyline(self):
        pass

    def preloop(self):
        self.tasks = TasksManager()

    def postloop(self):
        self.tasks.close()

    def do_q(self, empty):
        return True

    def do_mk(self, task_text):
        self.tasks.add(task_text)

    def do_rm(self, task_text):
        self.tasks.delete(task_text)

    def do_ed(self, task_uuid):
        new_task = raw_input('[Edit {}] {}'.format(task_uuid, self.prompt))
        self.tasks.edit(task_uuid, new_task)

    def do_mv(self, task):
        after = raw_input('[After] {}'.format(self.prompt))
        self.tasks.move_after(task, after)

    def do_ls(self, query):
        self._print_tasks(self.tasks.search(query) if query else self.tasks)


def run():
    CLI().cmdloop()


if __name__ == '__main__':
    run()
