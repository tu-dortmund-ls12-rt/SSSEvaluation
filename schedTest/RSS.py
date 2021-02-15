import math # math.ceil(), math.floor()

# Sorts the given task set by the execution time + suspension length in ascending order
# Input: Task set
# Output: Sorted Taskset
def sort_by_ex_and_susp(tasks): # lowest ex + susp first
    return sorted(tasks, key=lambda k: k['execution']+k['sslength'])

# Redundant Self Suspension Analyses 
# From: https://ieeexplore.ieee.org/abstract/document/9211430 Section V
# Input: Task set
# Output: Schedulability of the Task Set under RSS
def SC2EDF(tasks):
    htasks = sort_by_ex_and_susp(tasks)

    n = len(htasks)
    for l in range(n):
        U = 0
        for i in range(l):
            if htasks[l]['execution'] + htasks[l]['sslength'] >= htasks[i]['period']:
                # Compute Redundant suspension
                Rsus = (1.0/3.0) * (htasks[i]['period']/ htasks[l]['period']) * (math.floor((htasks[l]['execution']+htasks[l]['sslength'])/htasks[i]['period']) -1)
                # Compute relevant utilization
                U += ( htasks[i]['execution'] + (htasks[i]['sslength'] * (1.0 - Rsus)) ) / htasks[i]['period']
            else:
                # Compute suspension-oblivious utilization
                U += ( htasks[i]['execution']+htasks[i]['sslength'])/htasks[i]['period']
        # Add suspension-oblivious utilization of tau_l
        U += ( htasks[l]['execution']+htasks[l]['sslength'])/htasks[l]['period']
        # print(U)
        if U > 1:
            return False
    return True