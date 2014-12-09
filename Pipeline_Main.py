__author__ = 'Christopher Sheaf'

import sys
from xml.etree.ElementTree import ElementTree
from Pipeline_Core.TaskMaster import TaskMaster
from Pipeline_Tasks.Sequence_Variation import SequenceVariationTask
from Pipeline_Tasks.Homology_Modeling import HomologyModelingTask


def setup_task_dependencies(task_list):
    pass


def main():
    task_list = []
    master = TaskMaster()

    settings_xml = ElementTree.parse(sys.argv[1])  # Contains all the tasks that need to be run, and their parameters.
    for task_xml in settings_xml.findall('task'):
        task_name = task_xml.get('name')
        if task_xml.get('type') == 'SequenceVariationTask':
            task_list.append(SequenceVariationTask(task_name, master, task_xml))
        elif task_xml.get('type') == 'HomologyModelingTask':
            task_list.append(HomologyModelingTask(task_name, master, task_xml))

    setup_task_dependencies(task_list)
    master.add_task(task_list)

    master.run_tasks()

if __name__ == '__main__':
    main()