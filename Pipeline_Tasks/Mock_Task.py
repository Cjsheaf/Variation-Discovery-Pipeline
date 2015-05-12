__author__ = 'Christopher Sheaf'

from Pipeline_Core.Task import Task
from Pipeline_Core.TaskMaster import TaskMaster
import time


class MockTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(MockTask, self).__init__(task_name, task_master)
        self.run_time = int(xml_parameters.find('run_time').text)

    def run(self):
        time.sleep(self.run_time)