__author__ = 'Cjsheaf'

import shlex
from Pipeline_Core.Task import Task
from subprocess import check_output, CalledProcessError
from os import path, listdir
import posixpath
from fnmatch import fnmatch


class ResultsTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(ResultsTask, self).__init__(task_name, task_master)
        self.args = {}
        self.input_files = []
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        self.args['svl_filepath'] = xml_parameters.find('svl_filepath').text
        self.args['template_filepath'] = xml_parameters.find('template_filepath').text
        self.args['mdb_filepath'] = xml_parameters.find('mdb_filepath').text

        input_directory = xml_parameters.find('input_directory')
        self.args['input_path'] = input_directory.get('path')
        self.args['input_pattern'] = input_directory.find('pattern').text

    def collect_input_files(self):
        for file in listdir(self.args['input_path']):
            if fnmatch(file, self.args['input_pattern']):
                self.input_files.append(posixpath.join(self.args['input_path'], file))

    def write_rmsd(self, sequence_name, result_string):
        writer = self.task_master.get_results_writer()
        writer.put_rmsd(sequence_name, float(result_string))

    def write_compound_scores(self, sequence_name, result_string):
        lines = result_string.split('\n')
        scores = (lines[0], int(lines[1]), int(lines[2]), float(lines[3]), float(lines[4]),
                  float(lines[5]), float(lines[6]), float(lines[7]), float(lines[8]))

        writer = self.task_master.get_results_writer()
        writer.put_compound_scores(sequence_name, scores)

    def run(self):
        self.run_rmsd_scoring()
        self.run_compound_scoring()

    def run_rmsd_scoring(self):
        self.collect_input_files()

        for input_file in self.input_files:
            process_args = shlex.split(
                'moebatch -run "{script}" -rmsd {template} {other}'.format(
                    script=self.args['svl_filepath'],
                    template=self.args['template_filepath'],
                    other=input_file
                )
            )
            try:
                sequence_name = path.splittext(input_file)[0]
                output = check_output(process_args)
                self.write_rmsd(sequence_name, output)
            except CalledProcessError as e:
                # For some reason, moebatch seems to always return 1.
                if e.returncode != 1:  # Ignore a return code of 1.
                    raise e

    def run_compound_scoring(self):
        process_args = shlex.split(
            'moebatch -run "{script}" -compound {database}'.format(
                script=self.args['svl_filepath'],
                database=self.args['mdb_filepath']
            )
        )
        try:
            output = check_output(process_args)
            self.parse_results(output, 'compound')
        except CalledProcessError as e:
            # For some reason, moebatch seems to always return 1.
            if e.returncode != 1:  # Ignore a return code of 1.
                raise e