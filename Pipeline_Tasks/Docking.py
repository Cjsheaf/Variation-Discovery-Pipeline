__author__ = 'Cjsheaf'

import shlex
from Pipeline_Core.Task import Task
from subprocess import check_call, PIPE
from os import path, listdir
from fnmatch import fnmatch


class DockingTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(DockingTask, self).__init__(task_name, task_master)
        self.args = {}
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        pass

    def run(self):
        pass