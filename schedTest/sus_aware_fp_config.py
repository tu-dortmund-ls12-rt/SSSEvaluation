from schedTest import sus_aware_fp as our
from schedTest import tgPath as create

import numpy as np
import os
import sys
import random
import itertools
from itertools import repeat
from multiprocessing import Pool

#import plot  # plot results


random.seed(331)  # set seed to have same task sets for each plot


# def store_results(results, path, filename):
#     file = os.path.join(path, filename)
#     if not os.path.exists(path):
#         os.makedirs(path)
#     np.save(file, results)


# def load_results(path, filename):
#     file = os.path.join(path, filename)
#     results = np.load(file, allow_pickle=True)
#     return results


def config_created_tasks(taskset):
    deadline_stretch = [1, 1.3]
    # Deadline stretch
    if deadline_stretch != [1, 1]:    
        for tsk in taskset:
            mult = random.uniform(*deadline_stretch)
            tsk['deadline'] = tsk['period'] * mult
    # Sort by deadline
    taskset.sort(key=lambda x: x['deadline'])
    return taskset

def _test_scheme(taskset, gScheme):
    if gScheme == "exh":
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='exh')
    
    elif gScheme == "heuristic":
        # make arrival curve
        arr_curves = [our.arr_sporadic(task['period']) for task in taskset]
        # do sched test
        return our.sched_test(taskset, arr_curves, choose_xvec='lin')
     

# def test_scheme(gScheme, tasksets, multiproc=0):
#     '''Test a scheme for all tasksets in tasksets_difutil'''
#     print('Scheme:', gScheme)
#     results = []
#     acceptance = []
#     if multiproc == 0:  # without multiprocessing
#         for taskset in tasksets:
#             acceptance.append(_test_scheme(gScheme, taskset))
#     else:  # with multiprocessing
#         with Pool(multiproc) as p:
#             acceptance = p.starmap(
#                 _test_scheme, zip(repeat(gScheme), tasksets))
#     results.append(sum(acceptance)/len(tasksets))
 
#     return results





# def _set_deadlines(taskset, param):
#     for tsk in taskset:
#         tsk['deadline'] = tsk['period'] * param


# def _make_jitter_tasks(taskset, jit):
#     tasksetJ = [dict(tsk) for tsk in taskset]
#     for tsk in tasksetJ:
#         tsk['period'] *= (1-jit)
#     return tasksetJ


# def _constrained_tasks(taskset):
#     tasksetJ = [dict(tsk) for tsk in taskset]
#     for tsk in tasksetJ:
#         tsk['deadline'] = min(tsk['deadline'], tsk['period'])
#     return tasksetJ

