__author__ = 'Christopher Sheaf'

from threading import Thread


class Task (Thread):
    def __init__(self, task_name, task_master):
        super(Task, self).__init__()
        self.task_name = task_name
        self.dependencies = []
        self.task_master = task_master

    def run(self):
        pass  # Exists only to be implemented by subclasses of Task.

    def notify_taskmaster(self, message, value=None):
        self.task_master.notify(self, message, value)

    def depends_on(self, *other_tasks):
        if None in other_tasks:
            return
        self.dependencies.extend(other_tasks)

    def __str__(self):
        return self.task_name