__author__ = 'Christopher Sheaf'

import shlex
from Pipeline_Core.Task import Task
from subprocess import check_call, PIPE, CalledProcessError
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
        self.args['homology_options'] = posixpath.join(in_path, input_directory.find('homology_options').text)
        self.args['template_file'] = posixpath.join(in_path, input_directory.find('template_file').text)
        self.args['sequence_file'] = posixpath.join(in_path, input_directory.find('sequence_file').text)

        self.args['outputDir'] = xml_parameters.find('output_directory').text

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

        process_args = 'moebatch -run "{script}" -options "{options}" -template "{template}" -sequence "{sequence}" -out "{outDir}"'.format(
            script=self.args['svl_script_name'],  # The file will be accessed from the parent dir.
            options=posixpath.relpath(self.args['homology_options'], start=self.args['svl_directory']),
            template=posixpath.relpath(self.args['template_file'], start=self.args['svl_directory']),
            sequence=posixpath.relpath(self.args['sequence_file'], start=self.args['svl_directory']),
            outDir=posixpath.relpath(self.args['outputDir'], start=self.args['svl_directory'])
        )
        try:
            # This script currently outputs the homology model files in the directory where it was invoked.
            # Call the script from the output directory.
            check_call(process_args, stdout=PIPE, shell=True, cwd=self.args['svl_directory'])
        except CalledProcessError as e:
            # For some reason, moebatch seems to always return 1.
            if e.returncode != 1:  # Ignore a return code of 1.
                raise e
