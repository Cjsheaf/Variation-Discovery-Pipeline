__author__ = 'Cjsheaf'

import shlex
from Pipeline_Core.Task import Task
from subprocess import check_call, PIPE, CalledProcessError


class DockingTask(Task):
    def __init__(self, task_name, task_master, xml_parameters):
        super(DockingTask, self).__init__(task_name, task_master)
        self.args = {}
        self.parse_xml_parameters(xml_parameters)

    def parse_xml_parameters(self, xml_parameters):
        self.args['svl_filepath'] = xml_parameters.find('svl_filepath').text

        self.args['receptor'] = xml_parameters.find('receptor').text
        self.args['ligand'] = xml_parameters.find('ligand').text
        self.args['ph4'] = xml_parameters.find('pharmacophore').text
        self.args['output_filename'] = xml_parameters.find('output').text

    def run(self):
        process_args = shlex.split(
            'moebatch -run "{svl}" -receptor "{receptor}" -ligand "{ligand}" -ph4 "{ph4}" -out "{out}"'.format(
                svl=self.args['svl_filepath'],
                receptor=self.args['receptor'],
                ligand=self.args['ligand'],
                ph4=self.args['ph4'],
                out=self.args['output_filename']
            )
        )
        try:
            check_call(process_args, stdout=PIPE)
        except CalledProcessError as e:
            # For some reason, moebatch seems to always return 1.
            if e.returncode != 1:  # Ignore a return code of 1.
                raise e