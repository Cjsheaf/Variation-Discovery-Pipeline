__author__ = 'Cjsheaf'

import shlex
from Pipeline_Core.Task import Task
from subprocess import check_call, PIPE, CalledProcessError
from os import path, listdir
from fnmatch import fnmatch
import posixpath


class PDBExtractionTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(PDBExtractionTask, self).__init__(task_name, task_master)
        self.args = {}
        self.input_files = []
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        self.args['svl_filepath'] = xml_parameters.find('svl_filepath').text

        input_directory = xml_parameters.find('input_directory')
        self.args['input_path'] = input_directory.get('path')
        self.args['input_pattern'] = input_directory.find('pattern').text

        output_directory = xml_parameters.find('output_directory')
        out_path = output_directory.get('path')
        # TODO: Make 'append_filename' optional.
        self.args['append_filename'] = posixpath.join(out_path, output_directory.find('append_mdb').text)

    def collect_input_files(self):
        for file in listdir(self.args['input_path']):
            if fnmatch(file, self.args['input_pattern']):
                self.input_files.append(posixpath.join(self.args['input_path'], file))

    def run(self):
        self.collect_input_files()

        for input_file in self.input_files:
            process_args = shlex.split(
                'moebatch -run "{script}" -mdb "{input}" -pdb "{output}" -append "{append}"'.format(
                    script=self.args['svl_filepath'],
                    input=input_file,
                    output=posixpath.splitext(input_file)[0] + '.pdb',
                    append=self.args['append_filename']
                )
            )
            try:
                check_call(process_args, stdout=PIPE)
            except CalledProcessError as e:
                # For some reason, moebatch seems to always return 1.
                if e.returncode != 1:  # Ignore a return code of 1.
                    raise e
