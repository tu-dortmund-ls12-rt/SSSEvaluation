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

        interferences = count_interference(tasks, task['deadline'])

        if (task['execution'] + task['sslength'] + interferences) > task['deadline']:
            return False

    return True

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