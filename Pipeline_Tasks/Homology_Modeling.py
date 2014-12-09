__author__ = 'Christopher Sheaf'

from Pipeline_Core.Task import Task
from Pipeline_Core.TaskMaster import TaskMaster
import shlex
import subprocess
import os


class HomologyModelingTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(HomologyModelingTask, self).__init__(task_name, task_master)
        self.args = {}
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        pass

    def run(self):
        pass