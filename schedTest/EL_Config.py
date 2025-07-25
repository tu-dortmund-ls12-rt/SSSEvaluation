from schedTest import EL

def check(ischeme, tasks, EL_depth=None, EL_max_a=None):
    """Check function to apply multiprocessing."""

    # --- EL-DM Evaluation ---
    if ischeme == 'EL-DM':
        EL.set_prio(tasks, prio_policy=2)
        return EL.EL_fixed(tasks, depth=EL_depth)

    # --- EL-EDF Evaluation ---
    elif ischeme == 'EL-EDF':
        EL.set_prio(tasks, prio_policy=3)
        return EL.EL_fixed(tasks, depth=EL_depth)

    # --- EL-EQDF Variants ---
    elif ischeme == 'EL-EQDF-lam=0':
        EL.set_prio(tasks, prio_policy=101, lam=0)
        return EL.EL_fixed(tasks, depth=EL_depth)

    elif ischeme == 'EL-EQDF-lam=-1':
        EL.set_prio(tasks, prio_policy=101, lam=-1)
        return EL.EL_fixed(tasks, depth=EL_depth)

    elif ischeme == 'EL-EQDF-lam=+1':
        EL.set_prio(tasks, prio_policy=101, lam=+1)
        return EL.EL_fixed(tasks, depth=EL_depth)

    elif ischeme == 'EL-EQDF-any-lam-in-[-10,10]':
        for lam in [0] + list(range(-10, 11)):
            EL.set_prio(tasks, prio_policy=101, lam=lam)
            if EL.EL_fixed(tasks, depth=EL_depth):
                return True
        return False

    # --- EL-SAEDF Variants ---
    elif ischeme == 'EL-SAEDF-lam=0':
        EL.set_prio(tasks, prio_policy=201, lam=0)
        return EL.EL_fixed(tasks, depth=EL_depth)

    elif ischeme == 'EL-SAEDF-lam=-1':
        EL.set_prio(tasks, prio_policy=201, lam=-1)
        return EL.EL_fixed(tasks, depth=EL_depth)

    elif ischeme == 'EL-SAEDF-lam=+1':
        EL.set_prio(tasks, prio_policy=201, lam=+1)
        return EL.EL_fixed(tasks, depth=EL_depth)

    elif ischeme == 'EL-SAEDF-any-lam-in-[-10,10]':
        for lam in [0] + list(range(-10, 11)):
            EL.set_prio(tasks, prio_policy=201, lam=lam)
            if EL.EL_fixed(tasks, depth=EL_depth):
                return True
        return False

    # not an EL scheme
    else:
        raise ValueError(f"Unknown EL scheme: {ischeme}")