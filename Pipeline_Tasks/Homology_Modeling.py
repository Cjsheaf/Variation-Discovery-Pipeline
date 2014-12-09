__author__ = 'Christopher Sheaf'

import shlex
from Pipeline_Core.Task import Task
from Pipeline_Core.TaskMaster import TaskMaster
from subprocess import check_call, PIPE
from os import path


class HomologyModelingTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(HomologyModelingTask, self).__init__(task_name, task_master)
        self.args = {}
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        self.args['svl_filepath'] = xml_parameters.find('svl_filepath').text
        self.args['input_directory'] = xml_parameters.find('input_directory').get('path')

    def run(self):
        # MOE needs to be invoked from the directory containing the SVL scripts, otherwise it can't seem to
        # "find" the other SVL files. It would be nice to eliminate this issue and use absolute paths.
        process_args = shlex.split(
            'moe -load "{script}" -exec HomologyBatch [\'{input}\']'.format(
                script=path.basename(self.args['svl_filepath']),  # The file will be accessed from the parent dir.
                input=self.args['input_directory']
            )
        )
        check_call(process_args, stdout=PIPE, cwd=path.dirname(self.args['input_directory']))
