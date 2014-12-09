__author__ = 'Christopher Sheaf'

from Task import Task


class DependencyGraph:
    """A basic class that finds the order in which tasks must be executed, given an arbitrary number of tasks with
    no circular dependencies.

    Implemented by topologically sorting a Directed Acyclic Graph that represents the task dependencies.
    """
    def __init__(self, task_list):
        self.broken_links = []  # Used to make sure that all tasks listed as dependencies exist in the graph.
        self.dependencies = {}  # Copy of the dependencies listed in each Task object. Modified instead of those.
        self.graph = {}
        for task in task_list:
            self.__add_node(task)

        if len(self.broken_links) > 0:
            raise ValueError('Some Tasks listed as dependencies are missing! Make sure you include all dependencies!')

    def __add_node(self, task):
        # self.broken_links stores tasks that have not yet been found. Remove this task from self.broken_links.
        if task in self.broken_links:
            self.broken_links.remove(task)

        self.dependencies[task] = task.dependencies
        for dependency in task.dependencies:
            if dependency not in self.broken_links and task not in self.dependencies:
                self.broken_links.append(dependency)
            if dependency not in self.graph:
                self.graph[dependency] = [task]
            else:
                self.graph[dependency].append(task)

    def get_ready_tasks(self):
        while len(self.dependencies) > 0:
            result = []
            for dependency in self.dependencies:
                if len(self.dependencies[dependency]) == 0:
                    result.append(dependency)

            for dependency in result:
                if dependency in self.graph:
                    for task in self.graph[dependency]:
                        self.dependencies[task].remove(dependency)
                    del(self.graph[dependency])
                del(self.dependencies[dependency])

            yield result