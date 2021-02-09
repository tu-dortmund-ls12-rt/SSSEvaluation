import subprocess
import numpy as np
import time
import os
def tasks_out(tasks):
    list_tasks = []
    for c, task in enumerate(tasks):
        list_t = []
        for key in task:
            # keys: 'paths', 'Cseg', 'utilization', 'minSr', 'period', 'Sseg', 'deadline', 'sslength', 'execution'
            if key == 'Cseg' or key=='Sseg':
                list_t.append(len(task[key]))
                for value in task[key]:
                    list_t.append(value)
            elif key != 'paths':
                list_t.append(task[key])
        list_tasks.append(list_t)
    ar_t = np.asarray(list_tasks)
    if not os.path.exists("./rtss2016/"):
        os.makedirs("./rtss2016/")
    np.savetxt('./rtss2016/py_input.txt', ar_t, delimiter=',', fmt='%s')


def str_2_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False

def Biondi(tasks):
    tasks_out(tasks)
    #time.sleep(1)
    subprocess.call('./rtss2016/RTSS_FRED')

    with open('rt_result.txt', 'r') as file:
        an = file.read()
    accepted = str_2_bool(an)
    os.remove("rt_result.txt")
    return accepted
