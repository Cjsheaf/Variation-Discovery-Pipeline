__author__ = 'Christopher Sheaf'

import shlex
from Pipeline_Core.Task import Task
from Pipeline_Core.TaskMaster import TaskMaster
from subprocess import check_call, PIPE
from os import path


class SequenceVariationTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(SequenceVariationTask, self).__init__(task_name, task_master)
        self.args = {}
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        self.args['rscript_filepath'] = xml_parameters.find('rscript_filepath').text

        input_directory = xml_parameters.find('input_directory')
        in_path = input_directory.get('path')
        self.args['input_fasta'] = path.join(in_path, input_directory.find('fasta').text)
        self.args['position_matrix'] = path.join(in_path, input_directory.find('position_matrix').text)
        self.args['pam250'] = path.join(in_path, input_directory.find('pam250').text)

        output_directory = xml_parameters.find('output_directory')
        out_path = output_directory.get('path')
        self.args['output_fasta'] = path.join(out_path, output_directory.find('fasta').text)

        self.args['variation_rounds'] = int(xml_parameters.find('variation_rounds').text)
        self.args['num_variations'] = int(xml_parameters.find('num_variations').text)
        self.args['num_offspring'] = int(xml_parameters.find('num_offspring').text)
        self.args['pam_probability'] = int(xml_parameters.find('pam_probability').text)

    def run(self):
        process_args =shlex.split(
            'Rscript "{script}" "{input}" "{output}" "{matrix}" "{pam250}" {rounds} {variations} {offspring} {probability}'.format(
                script=self.args['rscript_filepath'],
                input=self.args['input_fasta'],
                output=self.args['output_fasta'],
                matrix=self.args['position_matrix'],
                pam250=self.args['pam250'],
                rounds=self.args['variation_rounds'],
                variations=self.args['num_variations'],
                offspring=self.args['num_offspring'],
                probability=self.args['pam_probability']
            )
        )
        check_call(process_args)