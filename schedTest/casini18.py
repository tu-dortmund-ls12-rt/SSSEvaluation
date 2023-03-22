# FROM https://ieeexplore.ieee.org/abstract/document/8603232 Section IV
# Partitioned Fixed-Priority Scheduling of Parallel Tasks Without Preemptions
# Daniel Casini, Alessandro Biondi, Geoffrey Nelissen, and Giorgio Buttazzo
# RTSS 2018
#
# Segmented self suspension for non-preemptive Fixed priority scheduling


import math


def _respA_B(taskset, i, k, t, Rbar):
    """Multiset that includes the k largest elements of C_i(t, Rbar) padded with zeros if C_i(t, Rbar) shorter than k elements. (Used in Lemma 2 and Theorem 1)"""
    # Define C_i(t, Rbar) (Equation 1)
    C = []
    for l in range(i + 1, len(taskset)):  # Lower priority tasks
        for j in range(len(taskset[l]["Cseg"])):  # Computation segments
            eta = 1 + math.floor(
                (t + Rbar[l][j] - taskset[l]["Cseg"][j]) / taskset[l]["period"]
            )
            for _ in range(eta):  # eta many duplicates
                C.append(taskset[l]["Cseg"][j])

    # take k largest
    C.sort(reverse=True)
    C = C[:k]

    while len(C) < k:
        C.append(0)

    return C


def _respA_I(taskset, i, t, Rbar):
    """Higher priority interference (Equation 2)"""
    # First part of minimum
    val1 = 0
    # for h in range(0, i + 1):  # Higher or equal priority including task i
    # (TODO: Should task i be included or not? I guess not but this is not clear from the text in the paper ...)
    for h in range(0, i):  # Higher or equal priority task different to task i
        for r in range(len(taskset[h]["Cseg"])):  # Computation segments
            mult = (
                math.floor(
                    (t + Rbar[h][r] - taskset[h]["Cseg"][r]) / taskset[h]["period"]
                )
                + 1
            )
            val1 += mult * taskset[h]["Cseg"][r]

    val2 = 0
    Rbarlast = [Rbar_lst[-1] for Rbar_lst in Rbar]
    Execsum = [sum(tsk["Cseg"]) for tsk in taskset]
    for h in range(
        0, i
    ):  # Higher or equal priority task different to task i # TODO same here
        mult = math.floor((t + Rbarlast[h] - Execsum[h]) / taskset[h]["period"]) + 1
        val2 += mult * Execsum[h]

    return min(val1, val2)


def _respA_rec(prev_res, taskset, idxtask: int, Rbar):
    task_under_analysis = taskset[idxtask]
    result = 0
    result += sum(task_under_analysis["Sseg"])
    result += sum(task_under_analysis["Cseg"][:-1])

    multiset = _respA_B(taskset, idxtask, len(taskset[idxtask]["Cseg"]), prev_res, Rbar)
    for b in multiset:
        result += b

    result += _respA_I(taskset, idxtask, prev_res, Rbar)

    return result


def _respA(taskset, idxtask: int, Rbar):
    """Theorem 1"""
    # Solve recursive R'_i
    prev_res = -1
    res = 0
    while prev_res < res:
        prev_res = res
        res = _respA_rec(prev_res, taskset, idxtask, Rbar)

    return res + taskset[idxtask]["Cseg"][-1]


def wcrt(taskset):
    """Worst-case response time analysis for a taskset.
    Assumptions:
        - Segmented self suspension
        - Non-preemptive FP scheduling (tasks ordered by priority)
    """
    # TODO: Implement


if __name__ == "__main__":
    # DEBUG
    debug_taskset = [
        {"period": 100, "Sseg": [2], "Cseg": [5, 10]},
        {"period": 500, "Sseg": [1, 2], "Cseg": [7, 1, 3]},
        {"period": 1000, "Sseg": [1, 2, 3], "Cseg": [2, 2, 5, 2]},
    ]
    debug_Rbar = [[10, 10], [50, 50, 50, 50], [100, 100, 100, 100]]
    print(_respA_B(debug_taskset, 0, 50, 200, debug_Rbar))
    print(_respA_I(debug_taskset, 2, 100, debug_Rbar))
    print(_respA(debug_taskset, 0, debug_Rbar))
    print(_respA(debug_taskset, 1, debug_Rbar))
    print(_respA(debug_taskset, 2, debug_Rbar))
