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
            # elif choose_xvec in [4, 'lin']:
            #     xveclist = Gen_xvec.heuristic2(taskset, wcrtlist)
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

    # def all_zero(list_length):
    #     return [[0] * list_length]

    # def all_one(list_length):
    #     return [[1] * list_length]

    # def heuristic1(taskset):
    #     '''Heuristic from the end of the technical report of 
    #     "A Unifying Response Time Analysis Framework for DynamicSelf-Suspending
    #     Tasks" by Chen, Nelissen, Huang in 20116'''
    #     vec = []
    #     for tsk in taskset:
    #         if tsk['sslength'] <= tsk['execution']:
    #             vec.append(1)
    #         else:
    #             vec.append(0)
    #     return [vec]

    # def heuristic2(taskset, wcrts):
    #     '''Linear approximation from the end of the technical report of 
    #     "A Unifying Response Time Analysis Framework for DynamicSelf-Suspending
    #     Tasks" by Chen, Nelissen, Huang in 20116'''

    #     vec_x = []
    #     sumU = 0

    #     for tsk, wcrt in zip(taskset, wcrts):
    #         indU = tsk['execution'] / tsk['period']  # compute util of task
    #         sumU += indU  # total util

    #         # lhs and rhs of eq 27
    #         lhs = indU * (wcrt - tsk['execution'])
    #         rhs = tsk['sslength'] * sumU

    #         if lhs > rhs:
    #             vec_x.append(1)
    #         else:
    #             vec_x.append(0)

    #     return [vec_x]


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


# def sota_CPA(
#         taskset,  # the taskset under analysis
#         arr_curves,  # list of arrival curve objects
#         upperbound_a=10,  # upper bound for the index a
#         # return response times instead of True, False is still returned:
#         flag_return_response=False
# ):
#     ''' State of the art for jitter based analysis (CPA).
#     '''
#     # WCRT list
#     wcrtlist = []

#     for ind, tsk in enumerate(taskset):

#         # analyse the task
#         task_wcrtlist = []

#         # (inda)-th job in a suspension-aware busy interval
#         for inda in itertools.count(start=1):
#             wcrt_bound_a = _sota_CPA_wcrtbound(
#                 ind, taskset, arr_curves, wcrtlist, inda)

#             task_wcrtlist.append(wcrt_bound_a)

#             # Check
#             if wcrt_bound_a > tsk['deadline'] or inda >= upperbound_a:
#                 return False
#             if wcrt_bound_a <= arr_curves[ind].arrival_time(inda) - arr_curves[ind].arrival_time(inda-1):
#                 break  # break a

#         wcrtlist.append(max(task_wcrtlist))  # add wcrt to list

#     if flag_return_response is True:
#         return wcrtlist
#     else:
#         return True


# def _sota_CPA_compute_interference(delta, tasks, WCRTs, arr_curves):
#     val = 0
#     for ind, wcrt in enumerate(WCRTs):
#         val += arr_curves[ind](delta + wcrt) * tasks[ind]['execution']
#     return val


# def _sota_CPA_wcrtbound(ind, taskset, arr_curves, wcrtlist, inda):
    tsk = taskset[ind]
    arrival_bound = arr_curves[ind].arrival_time(inda-1)
    theta = 0
    while True:
        lhs = inda * (tsk['execution'] + tsk['sslength']) + \
            _sota_CPA_compute_interference(
                theta, taskset, wcrtlist, arr_curves)

        resp = theta - arrival_bound

        if resp > tsk['deadline'] or lhs <= theta:
            break
        else:
            theta = lhs
    # breakpoint()

    return resp


# def sota_CPA(taskset, arr_curves):
#     def compute_interference(delta, tasks, WCRTs, arr_curves):
#         val = 0
#         for ind, wcrt in enumerate(WCRTs):
#             val += arr_curves[ind](delta + wcrt) * tasks[ind]['execution']
#         return val

#     WCRTs = []

#     for tsk in taskset:
#         theta = 0
#         while True:
#             lhs = tsk['execution'] + tsk['sslength'] + \
#                 compute_interference(theta, taskset, WCRTs, arr_curves)

#             if lhs > tsk['deadline']:
#                 return False
#             elif lhs <= theta:
#                 WCRTs.append(theta)
#                 break
#             else:
#                 theta = lhs

#     return True


#if __name__ == '__main__':
    # # Test all combinations:
    # print('=Test all combinations=')
    # for ell in range(4):
    #     print(ell, list(Gen_xvec.all_combinations(ell)))

    # # Test Qvec:
    # print('=Test Qvec=')
    # HPTasks = [
    #     {'sslength': 10},
    #     {'sslength': 30},
    #     {'sslength': 100}
    # ]
    # for xvec in Gen_xvec.all_combinations(3):
    #     print(xvec, _compute_qvec(HPTasks, xvec))

    # # Test arrival curve for sporadic:
    # print('=Test Arrival Curve for sporadic=')
    # arr_curve = arr_sporadic(3)
    # for delta in range(-10, 15):
    #     print(delta, arr_curve(delta))
    # for number in range(5):
    #     print(number, arr_curve.arrival_time(number))

    # # Test arrival curve for jitter:
    # print('=Test Arrival Curve for jitter=')
    # arr_curve = arr_jitter(4, 0.5)
    # for delta in range(-10, 15):
    #     print(delta, arr_curve(delta))
    # for number in range(5):
    #     print(number, arr_curve.arrival_time(number))

    # # Test compute A1:
    # print('=Test Compute A1=')
    # arr_curve = arr_sporadic(3)
    # for delta in range(0, 15):
    #     print(delta, _compute_A1(
    #         delta, {'period': 3, 'execution': 1}, arr_curve, 2))
    # for delta in range(0, 15):
    #     print(delta, _compute_A1(
    #         delta, {'period': 3, 'execution': 1}, arr_curve, 7))

    # # Test compute A0:
    # print('=Test Compute A0=')
    # arr_curve = arr_sporadic(3)
    # for delta in range(0, 15):
    #     print(delta, _compute_A0(
    #         delta, {'period': 3, 'execution': 1}, arr_curve, 2))
    # for delta in range(0, 15):
    #     print(delta, _compute_A0(
    #         delta, {'period': 3, 'execution': 1}, arr_curve, 7))

    # # Test schedulability test
    # print('=Test 1 schedulability test=')
    # taskset = []
    # taskset.append({'period': 4, 'deadline': 4,
    #                'execution': 1, 'sslength': 1})
    # taskset.append({'period': 10, 'deadline': 12,
    #                'execution': 2, 'sslength': 5})
    # taskset.append({'period': 100, 'deadline': 80,
    #                'execution': 10, 'sslength': 20})

    # arr_curves = [arr_sporadic(4), arr_sporadic(10), arr_sporadic(100)]

    # print(sched_test(taskset, arr_curves, choose_xvec=0, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=1, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=2, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=3, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=4, flag_return_response=True))

    # print('=Test 2 schedulability test=')
    # taskset = []
    # taskset.append({'period': 50, 'deadline': 200,
    #                'execution': 10, 'sslength': 10})
    # taskset.append({'period': 100, 'deadline': 200,
    #                'execution': 15, 'sslength': 15})
    # taskset.append({'period': 100, 'deadline': 300,
    #                'execution': 40, 'sslength': 20})

    # arr_curves = [arr_sporadic(50), arr_sporadic(100), arr_sporadic(100)]

    # print(sched_test(taskset, arr_curves, choose_xvec=0, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=1, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=2, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=3, flag_return_response=True))
    # print(sched_test(taskset, arr_curves, choose_xvec=4, flag_return_response=True))

    # print('=Test 3 sota cpa=')
    # taskset = []
    # taskset.append({'period': 50, 'deadline': 100,
    #                'execution': 10, 'sslength': 10})
    # taskset.append({'period': 100, 'deadline': 200,
    #                'execution': 15, 'sslength': 15})
    # taskset.append({'period': 100, 'deadline': 300,
    #                'execution': 40, 'sslength': 20})

    # arr_curves = [arr_sporadic(50), arr_sporadic(100), arr_sporadic(100)]

    # print(sota_CPA(taskset, arr_curves))
