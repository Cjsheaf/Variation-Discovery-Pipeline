__author__ = 'Cjsheaf'

import shlex
from Pipeline_Core.Task import Task
from subprocess import check_call, PIPE, CalledProcessError
from os import path, listdir
import posixpath
from fnmatch import fnmatch
from io import StringIO


class ResultsTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(RMSDTask, self).__init__(task_name, task_master)
        self.args = {}
        self.input_files = []
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        self.args['svl_filepath'] = xml_parameters.find('svl_filepath').text
        self.args['template_filepath'] = xml_parameters.find('template_filepath').text

        input_directory = xml_parameters.find('input_directory')
        in_path = input_directory.get('path')
        self.args['input_pattern'] = input_directory.find('pattern').text

    def collect_input_files(self):
        for file in listdir(self.args['input_path']):
            if fnmatch(file, self.args['input_pattern']):
                self.input_files.append(posixpath.join(self.args['input_path'], file))

    def parse_results(self, results):
        for line in results:
            print(line)

    def run(self):
        self.collect_input_files()

        for input_file in self.input_files:
            output = StringIO()

            process_args = shlex.split(
                'moebatch -run "{script}" {template} {other}'.format(
                    script=self.args['svl_filepath'],
                    template=self.args['template_filepath'],
                    other=input_file
                )
            )
            try:
                check_call(process_args, stdout=output)
                self.parse_results(output.getvalue())
            except CalledProcessError as e:
                # For some reason, moebatch seems to always return 1.
                if e.returncode != 1:  # Ignore a return code of 1.
                    raise e
            finally:
                output.close()
