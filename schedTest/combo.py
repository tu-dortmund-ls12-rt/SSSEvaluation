from __future__ import division
import math

def Workload_JitBlock(T, C, t, Q, y):
    # y is y_i and Q is calcualed beforehand
    return max(0,C*math.ceil((t+Q+(1-y)*(T-C))/T))

def TDAjitblock(task,HPTasks): #original design in RTAS2018
        vecY = [0 for j in range(len(HPTasks)+1)]
        C=task['execution']+task['sslength']
        R=C
        D=task['deadline']
        #decide the vector vec(y)
        Q = 0.0
        yk = 0
        for itask, y in zip(HPTasks, vecY):
            if itask['sslength'] <= itask['execution']:
                y = 1
            else:
                y = 0
            Q+=itask['sslength']*y
        if task['sslength'] < task['execution']:
            yk = 0
        while True:
            I=0
            for itask in HPTasks:
                I=I+Workload_JitBlock(itask['period'],itask['execution'],R, Q, yk)
            if R>D:
                return False
            if R < I+C:
                R=I+C
            else:
                return True
def sjsb(tasks):
    # note that tasks must be sorted according to periods. (RM)
    for i in range(len(tasks)):
        if TDAjitblock(tasks[i], tasks[:i]):
            continue
        else:
            return False
    return True
