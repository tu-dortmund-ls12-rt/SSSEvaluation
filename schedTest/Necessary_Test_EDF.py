"""
This is as a part of bachelor thesis of Zakaria Al-Jumaei.
Developing necessary test for EDF scheduling algorithm.
"""
from math import floor


def necessary_test_edf(tasks):
    """
    Input: task set that should be analysed
    Output: False > unschedulable , True > no decision
    """
    for index, task in enumerate(tasks):

        interferences = count_interference(index, tasks, task['deadline'])

        if (task['execution'] + task['sslength'] + interferences) > task['deadline']:
            return False

    return True

def count_interference(index, tasks, deadline):
    """
    count the number of interference of other tasks than task under analysis
    Input: index of task under analysis, task set, deadline of task under analysis
    Output: number of interference
    """
    interferences = 0
    for index_i, task in enumerate(tasks):
        if index_i == index:
            continue
        interferences += floor((deadline + task['sslength'] + (task['period'] - task['deadline']))
                               / task['period']) * task['execution']

    return interferences