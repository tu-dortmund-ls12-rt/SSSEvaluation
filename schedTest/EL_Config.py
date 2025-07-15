from schedTest import EL

def check(ischeme, tasks, EL_depth=None, EL_max_a=None):
    """Check function to apply multiprocessing."""
    numfail = 0
    # --- 1 DM Evaluation. ---
    if ischeme == 'EL-DM':  # EL scheduling
        EL.set_prio(tasks, prio_policy=2)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    # --- 2 EDF Evaluation. ---
    elif ischeme == 'EL-EDF':  # EL scheduling
        EL.set_prio(tasks, prio_policy=3)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    # --- 3 EQDF Evaluation. ---
    elif ischeme == 'EL-EQDF-lam=0':
        EL.set_prio(tasks, prio_policy=101, lam=0)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-EQDF-lam=-1':
        EL.set_prio(tasks, prio_policy=101, lam=-1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-EQDF-lam=+1':
        EL.set_prio(tasks, prio_policy=101, lam=+1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-EQDF-any-lam-in-[-10,10]':
        fail_flag = True
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            EL.set_prio(tasks, prio_policy=101, lam=lam)
            if EL.EL_fixed(tasks, depth=EL_depth) is True:
                fail_flag = False
                break
        if fail_flag:
            numfail += 1
    # --- 4 SAEDF Evaluation. ---
    elif ischeme == 'EL-SAEDF-lam=0':
        EL.set_prio(tasks, prio_policy=201, lam=0)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-SAEDF-lam=-1':
        EL.set_prio(tasks, prio_policy=201, lam=-1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-SAEDF-lam=+1':
        EL.set_prio(tasks, prio_policy=201, lam=+1)
        if EL.EL_fixed(tasks, depth=EL_depth) is False:
            numfail += 1
    elif ischeme == 'EL-SAEDF-any-lam-in-[-10,10]':
        fail_flag = True
        for lam in [0] + list(range(-10, 11, 1)):  # lam range
            # (Testing 0 first gives results faster.)
            EL.set_prio(tasks, prio_policy=201, lam=lam)
            if EL.EL_fixed(tasks, depth=EL_depth) is True:
                fail_flag = False
                break
        if fail_flag:
            numfail += 1
    else:
        raise ValueError(f"{ischeme=} is not a valid option.")

    return numfail