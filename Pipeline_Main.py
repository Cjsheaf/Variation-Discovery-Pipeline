__author__ = 'Christopher Sheaf'

import sys
import os
from Pipeline_Core.Util import confirm
import xml.etree.ElementTree as ETree
from Pipeline_Core.TaskMaster import TaskMaster
from Pipeline_Tasks.Sequence_Variation import SequenceVariationTask
from Pipeline_Tasks.Homology_Modeling import HomologyModelingTask
from Pipeline_Tasks.Mock_Task import MockTask
from Pipeline_Tasks.PDB_Extraction import PDBExtractionTask
from Pipeline_Tasks.Docking import DockingTask
from Pipeline_Tasks.Results import ResultsTask
# from playdoh import *


def find_matching_task(task_name, task_list):
    for task in task_list:
        if str(task) == task_name:
            return task
    return None


def setup_task_dependencies(task_list, settings_xml):
    for task_xml in settings_xml.findall('task'):
        parent = find_matching_task(task_xml.get('name'), task_list)
        if parent is None:
            raise RuntimeError(
                'Task "{name}" does not exist. It may have been improperly formatted, or may not have'
                ' been created properly.'.format(
                    name=task_xml.get('name')
                )
            )

        for dependency in task_xml.findall('dependency'):
            child = find_matching_task(dependency.get('name'), task_list)
            if child is None:
                raise RuntimeError(
                    'Could not find dependency named "{name}". Make sure the task exists and is'
                    ' formatted properly'.format(
                        name=dependency.get('name')
                    )
                )
            else:
                parent.depends_on(child)


def main():
    if not len(sys.argv) == 3:
        print('Please run this script with two arguments. The first being the file path to the settings'
              '\nxml, and the second being the file name of the results csv that will be created.')
        exit()

    task_list = []
    master = TaskMaster()

    settings_xml = ETree.parse(sys.argv[1])  # Contains all the tasks that need to be run, and their parameters.
    results_csv = sys.argv[2]

    # It's likely that an inexperienced user will not change the name of the results csv file.
    # Make the user aware that overwriting will occur, and default to not overwriting if the user
    # just mashes Enter, to avoid unintentionally deleting previous results.
    if os.path.exists(results_csv):
        overwrite_msg = 'The file: "{csv}" already exists. Overwrite? y/N?'.format(csv=results_csv)
        if not confirm(prompt=overwrite_msg, resp=False):  # Default to False
            exit()

    for task_xml in settings_xml.findall('task'):
        task_name = task_xml.get('name')
        task_type = task_xml.get('type')

        # At some point, it would be nice to replace this if-block with something that uses
        # reflection to find the appropriately-named Task class.
        if task_type == 'MockTask':
            task_list.append(MockTask(task_name, master, task_xml))
        elif task_type == 'SequenceVariationTask':
            task_list.append(SequenceVariationTask(task_name, master, task_xml))
        elif task_type == 'HomologyModelingTask':
            task_list.append(HomologyModelingTask(task_name, master, task_xml))
        elif task_type == 'PDBExtractionTask':
            task_list.append(PDBExtractionTask(task_name, master, task_xml))
        elif task_type == 'DockingTask':
            task_list.append(DockingTask(task_name, master, task_xml))
        elif task_type == 'ResultsTask':
            task_list.append(ResultsTask(task_name, master, task_xml))

    setup_task_dependencies(task_list, settings_xml)
    master.add_task(task_list)

    master.run_tasks()

if __name__ == '__main__':
    main()