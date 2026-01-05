# Schedulability test from "Suspension-Aware Fixed-Priority Schedulability Test 
# with Arbitrary Deadlines and Arrival Curves" Mario Günzel, Niklas Ueter, Jian-Jia Chen 2021.
#https://ieeexplore.ieee.org/abstract/document/9622374

import itertools
import math
import numpy as np


def _WCRT_bound(
    ind,  # index of task under analysis
    tasks,  # set of tasks
    arr,  # arrival curves
    xvec,  # vector of x
    wcrtvec,  # vector of WCRT bounds for higher priority tasks
    inda  # a-th job in suspension-aware busy interval
):
    '''Schedulability test from the paper, Thereom 17, Corollary 18.
    Assume that tasks are ordered by priority.

    Note that if the result is bigger than the task deadline, this 
    is not a real response time upper bound.'''

    task_an = tasks[ind]  # task under analysis
    HPTasks = tasks[:ind]  # higher priority tasks

    # Compute Qvec
    Qvec = _compute_qvec(HPTasks, xvec)

    # Compute lower bound on first time that arr curve is at least a:
    # This is the infimum from Eq (12)
    arrival_bound = arr[ind].arrival_time(inda-1)

    # kind of TDA
    theta = inda * (task_an['execution'] + task_an['sslength'])  # start

    while True:
        # compute left hand side of Eq (11)
        lhs = inda * (task_an['execution'] + task_an['sslength'])
        for idx, hptsk in enumerate(HPTasks):
            lhs += xvec[idx] * \
                _compute_A1(theta+Qvec[idx], hptsk, arr[idx], wcrtvec[idx])

            lhs += (1-xvec[idx]) * \
                _compute_A0(theta+Qvec[idx], hptsk, arr[idx], wcrtvec[idx])

        # check

        resp = theta - arrival_bound

        if resp > task_an['deadline']:
            break

        if lhs <= theta:  # wcrt upper bound found
            break

        theta = lhs  # increase theta

    return resp


def sched_test(
        taskset,  # the taskset under analysis
        arr_curves,  # list of arrival curve objects
        choose_xvec=0,  # choose xvectors from a predefined list
        own_xvec=None,  # set own list of xvectors
        upperbound_a=10,  # upper bound for the index a
        # return response times instead of True, False is still returned:
        flag_return_response=False
):
    ''' Schedulability test from COR18.
    Note: taskset has to be ordered by task priority
    Return: True = schedulable, False = no information
    '''
    # WCRT list
    wcrtlist = []

    for ind, tsk in enumerate(taskset):

        # set xvec list
        if own_xvec is None:
            if choose_xvec in [0, 'exh']:
                xveclist = Gen_xvec.all_combinations(len(taskset))
            # elif choose_xvec in [1, 'all0']:
            #     xveclist = Gen_xvec.all_zero(len(taskset))
            # elif choose_xvec in [2, 'all1']:
            #     xveclist = Gen_xvec.all_one(len(taskset))
            # elif choose_xvec in [3, 'SleqC']:
            #     xveclist = Gen_xvec.heuristic1(taskset)
            elif choose_xvec in [4, 'lin']:
                xveclist = Gen_xvec.heuristic2(taskset, wcrtlist)
            # elif choose_xvec in [5, 'comb3']:
            #     xveclist = (Gen_xvec.all_zero(len(taskset))
            #                 + Gen_xvec.all_one(len(taskset))
            #                 + Gen_xvec.heuristic2(taskset, wcrtlist))
        else:
            xveclist = own_xvec

        # analyse the task
        task_wcrtlist = []

        # (inda)-th job in a suspension-aware busy interval
        for inda in itertools.count(start=1):
            wcrt_bound_a = None

            for xvec in xveclist:
                # compute wcrt bound for this vec
                wcrt_bound_vec = _WCRT_bound(
                    ind, taskset, arr_curves, xvec, wcrtlist, inda)

                # update wcrt bound for index a
                if (wcrt_bound_a is None) or wcrt_bound_a > wcrt_bound_vec:
                    wcrt_bound_a = wcrt_bound_vec

            task_wcrtlist.append(wcrt_bound_a)

            # Check
            if wcrt_bound_a > tsk['deadline'] or inda >= upperbound_a:
                return False
            if wcrt_bound_a <= arr_curves[ind].arrival_time(inda) - arr_curves[ind].arrival_time(inda-1):
                break  # break a

        wcrtlist.append(max(task_wcrtlist))  # add wcrt to list

    if flag_return_response is True:
        return wcrtlist
    else:
        return True


class Gen_xvec:
    '''Collection of generators for xvectors.'''

    def all_combinations(list_length, entries=[0, 1]):
        '''Return all possible xvectors.'''
        return list(itertools.product(entries, repeat=list_length))

    def heuristic2(taskset, wcrts):
        '''Linear approximation from the end of the technical report of 
        "A Unifying Response Time Analysis Framework for DynamicSelf-Suspending
        Tasks" by Chen, Nelissen, Huang in 20116'''

        vec_x = []
        sumU = 0

        for tsk, wcrt in zip(taskset, wcrts):
            indU = tsk['execution'] / tsk['period']  # compute util of task
            sumU += indU  # total util

            # lhs and rhs of eq 27
            lhs = indU * (wcrt - tsk['execution'])
            rhs = tsk['sslength'] * sumU

            if lhs > rhs:
                vec_x.append(1)
            else:
                vec_x.append(0)

        return [vec_x]


def _compute_qvec(HPTasks, xvec):
    '''Compute the Qvector as in Lemma 16.'''
    Qvec = []
    Qvar = 0.0
    for idx, tsk in list(enumerate(HPTasks))[::-1]:
        Qvar += tsk['sslength']*xvec[idx]
        Qvec.insert(0, Qvar)

    return Qvec


def _compute_A1(
    delta,  # input
    taskj,  # task for the index
    arrj,  # arrival curve for the index
    wcrtj  # WCRT upper bound for the task with index
):
    res = delta
    res += max(wcrtj - taskj['period'], 0)
    res = arrj(res)
    res *= taskj['execution']

    return res


def _compute_A0(
    delta,  # input
    taskj,  # task for the index
    arrj,  # arrival curve for the index
    wcrtj,  # WCRT upper bound for the task with index
):
    Cstar = _compute_maxcurrwl(arrj, wcrtj, taskj['execution'])

    res = delta - taskj['period'] + wcrtj - Cstar
    res = arrj(res)
    res *= taskj['execution']
    res += Cstar

    # trivial bound
    res2 = arrj(delta + wcrtj) * taskj['execution']

    # return res
    return min(res, res2)


def _compute_maxcurrwl(
    arr_curve,  # arrival curve
    wcrt,  # WCRT upper bound
    wcet  # WCET upper bound
):
    val1 = arr_curve(wcrt) * wcet
    val2 = wcrt

    return min(val1, val2)


class ArrivalCurve:
    def __init__(self, func):
        self.base_function = func
        self.arrivals = []
        self.arrivals_gen = None

    def __call__(self, inputvalue):
        return self.base_function(inputvalue)

    def set_arrival_times(self, arrivallist):
        '''Set lower time bounds for the first arrivals.
        Arrivallist as generator.'''
        self.arrivals = arrivallist

    def set_arrival_times_gen(self, generator):
        '''Set lower time bounds for the first arrivals.
        Arrivallist as generator.'''
        self.arrivals_gen = generator

    def compute_first_arrivals(self, number, stepsize):
        '''Compute lower time bound for the first (number) arrivals.'''
        arrivallist = []
        tfloat = 0.0
        cmp_val = 1
        while cmp_val <= number:
            nxt = tfloat + stepsize  # compute next value
            if nxt >= cmp_val:
                arrivallist.append(tfloat)  # add to arrivallist
                cmp_val += 1
            tfloat = nxt

        self.arrivals = arrivallist

    def arrival_time(self, number):
        '''Lower bound on the arrival time of the (number)-th job 
        in a suspension-aware busy interval.
        Note: arrivals has to be computed or set.'''

        while True:
            if len(self.arrivals) > number:
                return self.arrivals[number]
            else:  # fill list using the generator
                self.arrivals.append(next(self.arrivals_gen))


def arr_sporadic(min_inter_arr):
    '''Returns the arrival curve for a sporadic task.'''
    def arr(delta):
        if delta <= 0:
            return 0
        else:
            return math.ceil(delta/min_inter_arr)

    def arr_times():
        timevar = 0.0
        while True:
            yield timevar
            timevar += min_inter_arr

    arr_curv = ArrivalCurve(arr)
    arr_curv.set_arrival_times_gen(arr_times())

    return arr_curv


def arr_jitter(min_inter_arr, jit):
    '''Returns the arrival curve for a task with jitter.'''
    def arr(delta):
        if delta <= 0:
            return 0
        else:
            return math.ceil((delta + jit*min_inter_arr)/min_inter_arr)

    def arr_times():
        timevar = 0.0
        yield timevar
        timevar += (1-jit) * min_inter_arr
        while True:
            yield timevar
            timevar += min_inter_arr

    arr_curv = ArrivalCurve(arr)
    arr_curv.set_arrival_times_gen(arr_times())

    return arr_curv


def arr_log(min_inter_arr):
    '''Returns the logarithmic arrival curve for a task.'''
    def arr(delta):
        if delta <= 0:
            return 0
        else:
            return np.log(delta+1)/np.log(min_inter_arr+1) + 1

    def arr_times():
        for ind in itertools.count(start=1):
            timevar = (ind-1)*np.log(min_inter_arr+1)
            timevar = np.exp(timevar) - 1
            yield timevar

    arr_curv = ArrivalCurve(arr)
    arr_curv.set_arrival_times_gen(arr_times())

    return arr_curv

