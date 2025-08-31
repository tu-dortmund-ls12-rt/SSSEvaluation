"""
This is as a part of bachelor thesis of Zakaria Al-Jumaei.
Developing necessary test for EDF scheduling algorithm,
in order to evaluate the gab between this test and the sufficient test that provided by paper:
Response-Time Analysis for Self-Suspending Tasks
Under EDF Scheduling. Federico Aromolo, Alessandro Biondi, Geoffrey Nelissen
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECRTS.2022.13
"""
from math import floor
import copy


def necessary_test_edf(tasks):
    """
    Input: task set that should be analysed
    Output: False > unschedulable , True > no decision
    """
    for index, task in enumerate(tasks):

        task_set_new = align_deadline(tasks, index, task)

        interferences = count_interference(task_set_new, task['deadline'])

        if (task['execution'] + task['sslength'] + interferences) > task['deadline']:
            return False

    return True

def align_deadline(tasks, index, task_k):
    """
    align deadline of other task with deadline of task under analysis.
    Input: taskset
    Output: taskset after aligning deadline
    """
    others = [copy.copy(t) for i, t in enumerate(tasks) if i != index]

    for task_i in others:
        task_i['deadline'] = task_k['deadline']
    return others

def count_interference(tasks, deadline):
    """
    count the number of interference of other tasks than task under analysis
    Input: task set after aligning deadline and without task under analysis
    Output: number of interference
    """
    interferences = 0
    for task in tasks:
        interferences += floor((deadline + task['sslength']) / task['period']) * task['execution']

    return interferences