__author__ = 'Christopher Sheaf'

import shlex
from Pipeline_Core.Task import Task
from Pipeline_Core.TaskMaster import TaskMaster
import time
from subprocess import check_call, PIPE


class MockTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(MockTask, self).__init__(task_name, task_master)
        self.run_time = int(xml_parameters.find('run_time').text)

    def run(self):
        print('Running "{name}" for {time} seconds.'.format(name=self.task_name, time=self.run_time))
        check_call(shlex.split('sleep {time}s'.format(time=self.run_time)), stdout=PIPE)
        print('{name} complete.'.format(name=self.task_name))