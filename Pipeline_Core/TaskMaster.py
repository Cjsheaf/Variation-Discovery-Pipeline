__author__ = 'Christopher Sheaf'

from collections import Iterable
from Pipeline_Core.DependencyGraph import DependencyGraph


class TaskMaster:
    def __init__(self):
        self.task_list = []
        self.dependency_graph = None
        self.running_tasks = []

    def add_task(self, task):
        if isinstance(task, Iterable):
            self.task_list.extend(task)
        else:
            self.task_list.append(task)

    def run_tasks(self):
        self.dependency_graph = DependencyGraph(self.task_list)

        for batch in self.dependency_graph.get_ready_tasks():
            for task in batch:
                self.running_tasks.append(task)
                task.start()
            for task in list(self.running_tasks):  # Iterate over a copy of the list
                task.join()
                self.running_tasks.remove(task)

    # The notifier is a reference to the caller of this method. The message denotes what
    # event has occurred, and value (optional) is message-dependent (E.G: A message of
    # "Error Encountered" might set it to a string or integer representing the error).
    def notify(self, notifier, message, value=None):
        # Does not work. The exception is still raised in the caller thread. Need a better way to propagate errors.
        if message == 'Error':
            raise value  # value should be an exception object