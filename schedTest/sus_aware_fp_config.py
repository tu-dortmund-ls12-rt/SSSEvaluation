from schedTest import sus_aware_fp as our

import random


random.seed(331)  # set seed to have same task sets for each plot

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
