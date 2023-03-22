# FROM https://ieeexplore.ieee.org/abstract/document/8603232 Section IV
# Partitioned Fixed-Priority Scheduling of Parallel Tasks Without Preemptions
# Daniel Casini, Alessandro Biondi, Geoffrey Nelissen, and Giorgio Buttazzo
# RTSS 2018
#
# Segmented self suspension for non-preemptive Fixed priority scheduling


import math


def _respA_B(taskset, i, k, t, Rbar):
    """Multiset that includes the k largest elements of C_i(t, Rbar) padded with zeros if C_i(t, Rbar) shorter than k elements."""
    # Define C_i(t, Rbar)
    C = []
    for l in range(i + 1, len(taskset)):  # lower priority tasks
        for j in range(len(taskset[l]["Cseg"])):
            eta = 1 + math.floor(
                (t + Rbar[l][j] - taskset[l]["Cseg"][j]) / taskset[l]["period"]
            )
            for _ in range(eta):
                C.append(taskset[l]["Cseg"][j])

    # take k largest
    C.sort(reverse=True)
    C = C[:k]

    while len(C) < k:
        C.append(0)

    return C


def _respA_rec(taskset, idxtask: int):
    task_under_analysis = taskset[idxtask]
    result = 0
    result += sum(task_under_analysis["Sseg"])
    result += sum(task_under_analysis["Cseg"][:-1])


def _respA(
    taskset,
    idxtask: int,
):
    """Theorem 1"""


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
        {"period": 10, "Sseg": [2], "Cseg": [5, 10]},
        {"period": 50, "Sseg": [1, 2], "Cseg": [7, 1, 3]},
        {"period": 100, "Sseg": [1, 2, 3], "Cseg": [2, 2, 5, 2]},
    ]
    debug_Rbar = [[10, 10], [50, 50, 50, 50], [100, 100, 100, 100]]
    print(_respA_B(debug_taskset, 0, 50, 200, debug_Rbar))
