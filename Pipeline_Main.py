__author__ = 'Christopher Sheaf'

import sys
import xml.etree.ElementTree as ETree
from Pipeline_Core.TaskMaster import TaskMaster
from Pipeline_Tasks.Sequence_Variation import SequenceVariationTask
from Pipeline_Tasks.Homology_Modeling import HomologyModelingTask
from Pipeline_Tasks.Mock_Task import MockTask
from Pipeline_Tasks.PDB_Extraction import PDBExtractionTask
from Pipeline_Tasks.Docking import DockingTask
from Pipeline_Tasks.RMSD import RMSDTask
from playdoh import *


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
    task_list = []
    master = TaskMaster()

    settings_xml = ETree.parse(sys.argv[1])  # Contains all the tasks that need to be run, and their parameters.
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
        elif task_type == 'RMSDTask':
            task_list.append(RMSDTask(task_name, master, task_xml))

    setup_task_dependencies(task_list, settings_xml)
    master.add_task(task_list)

    master.run_tasks()

if __name__ == '__main__':
    main()