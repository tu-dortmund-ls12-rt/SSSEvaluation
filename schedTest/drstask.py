from __future__ import division
import random
import math
import sys, getopt
import json
import datetime
from drs import drs

DRS_exe = []
DRS_val = []
Task = []

#   DRS_exe[], DRS_val[] and Task[] are varaibles of list type


def Period_generate(Pmin, numLog, val_ex, val_sus):
    j = 0
    temp = 0
    for i in val_ex:

        thN = j % numLog
        p = random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))

        # generates period values which are later multiplied with entries from val_ex, val_sus to 
        # produce execution and suspension values respectively

        pair = {}
        pair['period'] = p
        pair['execution'] = i*p
        pair['suspension'] = p*val_sus[temp]
        Task.append(pair)
        temp = temp + 1
        j = j+1

    return Task

#   returns task sets with values {period, execution, suspension}


def DRS_ex_sus(n, util_ex_Sus, ubound, lbound):

    #   generates the U^execution + suspension vector

    return drs(n, util_ex_Sus, ubound, lbound)


def DRS_ex(n, util_Ex, ubound_exe_sus, lbound):

    #   generates the U^execution taking U^execution + suspension vector as an upper_bound

    return drs(n, util_Ex, ubound_exe_sus, lbound)


def taskGeneration_drs(NumberOfTasksPerSet, uTotal_Exe_Sus,
                       uTotal_Exe, u_Bound, l_Bound, Pmin=100, numLog=1):

    val_exe_sus = DRS_ex_sus(NumberOfTasksPerSet, uTotal_Exe_Sus, u_Bound, l_Bound)
    # u_bound takes value between 0-1
    # uTotal_Exe_Sus takes value between 0-n

    val_ex = DRS_ex(NumberOfTasksPerSet, uTotal_Exe, val_exe_sus, l_Bound)
    # uTotal_Exe takes value <=1 & l_Bound <= uTotalSus <= u_Bound
    # u_bound will be the vector obtained from DRS_ex_sus

    val_sus = []
    sus_object = zip(val_exe_sus, val_ex)
    for item1, item2 in sus_object:
        val_sus.append(item1 - item2)

    Period_generate(Pmin, numLog, val_ex, val_sus)
    print('Number of tasks:', len(Task))
    return Task


if __name__ == '__main__':
    # DEBUG
    print('Randomly generate 10 tasks ...')

    ts = taskGeneration_drs(10, 2, 1, [0.3] * 10, [0.05] * 10)

    print('')
    print(ts)
    print('')
    print('number of tasks:', len(ts))
    print('the first task:', ts[1])
    print('the last task:', ts[-1])

    breakpoint()  # here you can have a deeper look into the task set 'ts'. Quit with 'q'
