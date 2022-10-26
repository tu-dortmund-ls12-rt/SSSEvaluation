from __future__ import division
import random
import math
import sys, getopt
import json
import datetime
from drs import drs



def Period_generate(Pmin, numLog, val_ex, val_sus):
    """ Generates the Period values and returns the final Taskset

    Args:
        Pmin (int) : Takes a set value of 100
        numLog (int) : Takes a pre-set value of 1
        val_ex (list) : List of execution values
        val_sus (list) : List of suspension values

    Returns:
        Task (list): Returns an appended list of Task-set in the form: {period, execution, suspension}

    """
    Task = []
    j = 0
    temp = 0
    for i in val_ex:

        thN = j % numLog
        p = random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
        pair = {}
        pair['period'] = p
        pair['execution'] = i*p
        pair['sslength'] = p*val_sus[temp]
        # pair['cseg'] = value_csegements
        # pair['sseg'] = value_suspsegments
        Task.append(pair)
        temp = temp + 1
        j = j+1

        # pair['cseg'] = value_csegements
        # pair['sseg'] = value_suspsegments    

    return Task


def DRS_ex_sus(n, util_ex_Sus):
    """ Generates and returns the Utilization vector for execution and suspension time combined

    Args:
        n (int) : Number of tasks
        util_ex_Sus (float) : Sum of all utilisation values(<= Number Of Tasks) for execution and suspension

    Returns:
        drs (list): Returns a vector of n number of utilization values for (execution + suspension) time

    """

    return drs(n, util_ex_Sus)


def DRS_ex(n, util_Ex, ubound_exe_sus):
    """ Generates and returns the Utilization vector for execution

    Args:
        n (int) : Number of tasks
        util_Ex (float) : Total utilisation value(<=1) for execution
        ubound_exe_sus (float) : Every utilization value has its Upperbound set
                                to the utilization values generetaed by DRS_ex_sus function

    Returns:
        drs (list): Returns a vector of n number of utilization values for exeecution time
        NB: Keeping util_Ex as 0 will produce an array of 0s of size 'n'
    """
   
    if util_Ex == 0:
        exception = []
        for i in range(n):
            bucket = i * 0
            exception.append(bucket)

        return exception

    else:
        return drs(n, util_Ex, ubound_exe_sus)


def execution_segments(n, ExUtil):

    return drs(n, ExUtil)


def suspension_segments(n, SusUtil):
    
    tasks = n-1

    return drs(tasks, SusUtil)


def taskGeneration_drs(NumberOfTasksPerSet, uTotal_Exe_Sus,
                       uTotal_Exe, Pmin=100, numLog=1, number_segments=2):
    """ Generates and returns the tasksets

    Args:
        NumberOfTasksPerSet (int) : Total number of tasks
        uTotal_Exe_Sus (float) : Sum of all utilisation values(>=1 is possible) for execution and suspension
        uTotal_Exe (float) : Total utilisation value(<=1) for execution
        NB: uTotal_Exe_Sus must be >= uTotal_Exe

    Returns:
        Task_set (list): Returns the final Task-set
    """

    val_exe_sus = DRS_ex_sus(NumberOfTasksPerSet, uTotal_Exe_Sus)
    #print(val_exe_sus)
    val_ex = DRS_ex(NumberOfTasksPerSet, uTotal_Exe, val_exe_sus)
    val_sus = []
    sus_object = zip(val_exe_sus, val_ex)
    for item1, item2 in sus_object:
        val_sus.append(item1 - item2)
    
    Task_set = Period_generate(Pmin, numLog, val_ex, val_sus)

    Task_set = implicit_deadline(Task_set)

    Task_set = segments(Task_set, number_segments)


    return Task_set


def implicit_deadline(ts):
    for tsk in ts:
        tsk['deadline'] = tsk['period']
    return ts


def segments(ts, number_segments):

    modify_list = [(task, execution_segments(number_segments, task['execution']), suspension_segments(number_segments, task['sslength'])) for task in ts]

    ts = [d | {"Cseg": exec_segments, "Sseg": sus_segments} for d, exec_segments, sus_segments in modify_list]

    return ts



if __name__ == '__main__':
    # DEBUG
    print('Randomly generating tasks ...')

    ts = taskGeneration_drs(10, 2, 1 )

    print('')
    print(ts)
    print('')
    # print('number of tasks:', len(ts))
    # print('the first task:', ts[1])
    # print('the last task:', ts[-1])
 
    breakpoint()