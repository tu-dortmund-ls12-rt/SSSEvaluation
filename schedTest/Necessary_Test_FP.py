"""
This is as a part of bachelor thesis of Zakaria Al-Jumaei.
Developing necessary test for fixed-priority scheduling algorithm.
"""
import math


def necessary_test_fp(tasks):
    """
    Input:Set of tasks
    Output:False -> unschedulable, True -> no decision
    """
    for index, task in enumerate(tasks):
        t = 0
        while(True):
            #interference from each higher-priority task
            demand = demand_hp(tasks[:index], t)

            t_new = task['execution'] + task['sslength'] + demand
            if t_new > task['deadline']:
                return False
            if t_new <= t:
                break #no detecting any deadline miss, continue with the next task.
            t = t_new

    return True

def demand_hp(tasks_hp, t):
    """
    Input:
    tasks_hp = Set of high priority tasks
    t = response time

    output: wcrt of higher priority tasks
    """
    demand = 0
    for task in tasks_hp:
        demand += math.ceil((t + task['sslength']) / task['period']) * task['execution']

    return demand