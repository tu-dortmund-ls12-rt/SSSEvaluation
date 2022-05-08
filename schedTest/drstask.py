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


def Period_generate(Pmin, numLog, DRS_val, DRS_exe):
    j = 0
    temp = 0
    for i in DRS_exe:

        thN = j % 1
        p = random.uniform(100*math.pow(10, thN), 100*math.pow(10, thN+1))

        # generates period values which are later multiplied with 
        # DRS_exe util values and DRS_val util values to generate
        # WCET and Suspension values respectively

        pair = {}
        pair['period'] = p
        pair['execution'] = i*p
        pair['suspension'] = p*DRS_val[temp]
        Task.append(pair)
        temp = temp + 1
        j = j+1

    return Task

#   returns task sets with values {period, execution, suspension}


def DRS_wcet(n, util_Exe, ubound, lbound):

    #   generates utilization values to calculate WCET

    return drs(n, util_Exe, ubound, lbound)


def DRS_sus(n, util_Sus, ubound, lbound):

    #   generates utilization values to calculate suspension time

    return drs(n, util_Sus, ubound, lbound)


def taskGeneration_drs(NumberOfTasksPerSet, uTotalExe,
                       uTotalSus, u_Bound, l_Bound, Pmin=100, numLog=1):

    DRS_exe = DRS_wcet(NumberOfTasksPerSet, uTotalExe, u_Bound, l_Bound)
    # uTotalExe takes a value <=1 & l_Bound <= uTotalExe <= u_Bound
    DRS_val = DRS_sus(NumberOfTasksPerSet, uTotalSus, u_Bound, l_Bound)
    # uTotalSus can take value more than 1 & l_Bound <= uTotalSus <= u_Bound
    Period_generate(Pmin, numLog, DRS_val, DRS_exe)

    print('number of tasks:', len(Task))
    return Task


if __name__ == '__main__':
    # DEBUG
    # Start this script with:
    # python3 -m schedTest.drstask
    print('Randomly generate 10 tasks ...')

    ts = taskGeneration_drs(10, 0.9, 2, [0.3]*10, [0.05]*10)

    print('')
    print(ts)
    print('')
    print('number of tasks:', len(ts))
    print('the first task:', ts[1])
    print('the last task:', ts[-1])

    breakpoint()
