__author__ = 'Christopher Sheaf'

import shlex
from Pipeline_Core.Task import Task
from Pipeline_Core.TaskMaster import TaskMaster
from subprocess import check_call, PIPE
from os import path
import posixpath


class HomologyModelingTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(HomologyModelingTask, self).__init__(task_name, task_master)
        self.args = {}
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        self.args['svl_script_name'] = path.basename(xml_parameters.find('svl_filepath').text)
        self.args['svl_directory'] = path.dirname(xml_parameters.find('svl_filepath').text)

        input_directory = xml_parameters.find('input_directory')
        in_path = input_directory.get('path')
        self.args['homology_options'] = path.join(in_path, input_directory.find('homology_options').text)
        self.args['template_file'] = path.join(in_path, input_directory.find('template_file').text)
        self.args['sequence_file'] = path.join(in_path, input_directory.find('sequence_file').text)

    def run(self):
        # MOE needs to be invoked from the directory containing the SVL scripts, otherwise it can't seem to
        # "find" the other SVL files. It would be nice to eliminate this issue and use absolute paths.
        #lex = shlex.shlex(
        #    'moe -load "{script}" -exec "HomologyBatch [\'{input}\']"'.format(
        #        script=self.args['svl_script_name'],  # The file will be accessed from the parent dir.
        #        # MOE only accepts POSIX-like file paths as SVL function arguments.
        #        input=posixpath.relpath(self.args['input_directory'], start=self.args['svl_directory'])
        #    )
        #)
        #lex.whitespace_split = True
        #process_args = list(lex)
        #check_call(process_args, stdout=PIPE, cwd=self.args['svl_directory'])

        process_args = 'moe -load "{script}" -exec "HomologyBatch_NoGUI [\'{options}\', \'{template}\', \'{sequence}\']"'.format(
            script=self.args['svl_script_name'],  # The file will be accessed from the parent dir.
            options=posixpath.relpath(self.args['input_directory'], start=self.args['homology_options']),
            template=posixpath.relpath(self.args['input_directory'], start=self.args['template_file']),
            sequence=posixpath.relpath(self.args['input_directory'], start=self.args['sequence_file'])
        )
        check_call(process_args, stdout=PIPE, shell=True, cwd=self.args['svl_directory'])
