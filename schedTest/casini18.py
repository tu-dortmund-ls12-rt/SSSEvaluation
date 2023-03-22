# FROM https://ieeexplore.ieee.org/abstract/document/8603232 Section IV
# Partitioned Fixed-Priority Scheduling of Parallel Tasks Without Preemptions
# Daniel Casini, Alessandro Biondi, Geoffrey Nelissen, and Giorgio Buttazzo
# RTSS 2018
#
# Segmented self suspension for non-preemptive Fixed priority scheduling


import math


def _multisetB(taskset, i, k, t, Rbar):
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


def _interference_I(taskset, i, t, Rbar):
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
    """Recursive definition of R'_i from Equation 4."""
    task_under_analysis = taskset[idxtask]
    result = 0
    result += sum(task_under_analysis["Sseg"])
    result += sum(task_under_analysis["Cseg"][:-1])

    multiset = _multisetB(
        taskset, idxtask, len(taskset[idxtask]["Cseg"]), prev_res, Rbar
    )
    for b in multiset:
        result += b

    result += _interference_I(taskset, idxtask, prev_res, Rbar)

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


def _rik(i, k, Rbar, taskset):
    """r_{i,k} from Lemma 4."""
    if k == 0:
        return 0
    else:
        return Rbar[i][k - 1] + taskset[i]["Sseg"][k - 1]


def _respB_rec_Delta(taskset, prev_res, i, b, Rbar):
    """Recurse definition of Delta_i from Equation 6."""
    return b + _interference_I(taskset, i, prev_res, Rbar)


def _respB(taskset, idxtask, idxseg, Rbar):
    """Theorem 2"""
    result = 0
    for iseg in range(idxseg + 1):  # Computation segments
        result += taskset[idxtask]["Cseg"][iseg]
    for iseg in range(idxseg):  # Suspension segments
        result += taskset[idxtask]["Sseg"][iseg]

    rik = _rik(idxtask, idxseg, Rbar, taskset)
    multiset = _multisetB(taskset, idxtask, idxseg, rik, Rbar)

    for b in multiset:
        # solve recursive Delta_i
        prev_res = -1
        res = 0
        while prev_res < res:
            prev_res = res
            res = _respB_rec_Delta(taskset, prev_res, idxtask, b, Rbar)
        result += res

    return result


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
    print(_multisetB(debug_taskset, 0, 50, 200, debug_Rbar))
    print(_interference_I(debug_taskset, 2, 100, debug_Rbar))
    print("")
    print(_respA(debug_taskset, 0, debug_Rbar))
    print(_respA(debug_taskset, 1, debug_Rbar))
    print(_respA(debug_taskset, 2, debug_Rbar))
    print("")
    print(_respB(debug_taskset, 0, len(debug_taskset[0]["Cseg"]) - 1, debug_Rbar))
    print(_respB(debug_taskset, 1, len(debug_taskset[1]["Cseg"]) - 1, debug_Rbar))
    print(_respB(debug_taskset, 2, len(debug_taskset[2]["Cseg"]) - 1, debug_Rbar))
