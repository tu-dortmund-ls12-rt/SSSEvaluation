import math
from bisect import bisect_left
from bisect import insort_left 

# Synchronous Release Sequence Refinement
# From: https://dl.acm.org/doi/abs/10.1145/2997465.2997485
# Input: Task set
# Output: Schedulability of the Task Set under SRSR
def SRSR(tasks):    
    len_tasks = len(tasks)
    # Assumption: All higher priority tasks are non-suspending
    # Work through taskset-subsets to determine schedulability
    # Conversion of Suspending tasks to non-suspending:
    # ExecutionTime = Sum(Execution-Segments)+Suspension Segment
    for i in range(len_tasks):
        subtasks = tasks[0:i]
        task = tasks[i]
        if not SRSR_n(subtasks,task):
           return False
    return True


# Input: Non-suspending task-set and suspending task
# Output: Schedulability of the task regarding higher-priority task-set
def SRSR_n(tasks,task):
    # Determine segments which each higher priority can interfere with
    syn = [12 for t in tasks]
    todo = [syn]
    offset = [0] * len(tasks)
    # Calculate maximum number of interferences by higher priority tasks
    NIup = maxRels(tasks, task['Cseg'][0],offset)
    while len(todo) > 0:
        head = todo.pop()
        processedNI = []
        # Calculate response time of task
        rt = RespTime(tasks, task, offset, NIup, head, processedNI)
        if rt > task['deadline']:
            if isAbst(head):
                #do a refinement step if abstract
                ind = selectToRefine(head, tasks)
                syn1 = list(head)
                syn2 = list(head)
                syn1[ind] = 1
                syn2[ind] = 2
                todo.append(syn1)
                todo.append(syn2)
            else:
                # counter example found without any further refinement possible
                return False
    return True

# Input: Lists a and x
# Output: Is x element of a?
def contains(a, x):
    'Locate the leftmost value exactly equal to x'
    i = bisect_left(a, x)
    if i != len(a) and a[i] == x:
        return True
    return False

# Input: Taskset, task, offset of tasks, Interferences, Segments, Processed Interferences
# Output: Response time of task
def RespTime(tasks, task, offset, NIup, syn, processedNI):
    # to avoid redundant calls
    if contains(processedNI, NIup) == True:
        # print 'already processed ' + str(len(processedNI))
        return 0
    insort_left(processedNI, NIup)

    offset = [0] * len(tasks)
        
    UBss  = wcrt(task['Cseg'][0]+task['Sseg'][0]+task['Cseg'][1], tasks,offset)
    UBss2 = wcrt(task['Cseg'][1], tasks,offset)
    
    n = len(tasks)
    Rss1bwd = 0
    NI = list(NIup)
    Rss1 = task['Cseg'][0] + sum([NIup[k]*(sum(tasks[k]['Cseg'])+tasks[k]["sslength"]) for k in range(n)])

    while Rss1bwd != Rss1:
        Rss1bwd = Rss1
        for k in range(n):
            if syn[k] == 2: # the task belongs to Sync2
                if NI[k] > (Rss1 + task['Sseg'][0] + 0.0) / tasks[k]['period']:
                    NI[k] = NI[k] - 1
                    
        # compute the response time of tau_{n,1}:
        rels = [min(NI[k], math.ceil( (Rss1 + 0.0) / tasks[k]['period']))  for k in range(n)]
        Rss1 = task['Cseg'][0] + sum([rels[k]*(sum(tasks[k]['Cseg'])+tasks[k]["sslength"]) for k in range(n)])  + 0.0
        for k in range(n):
            NI[k] = min(NI[k], math.ceil( (Rss1 + 0.0) / tasks[k]['period'])) # seemed incomplete in the paper
            
    # compute the offsets with \tau_{n,2}
    for k in range(n):
        if syn[k] == 12 or syn[k] == 2:
            offset[k] = 0
        else:
            offset[k] = max(0, NI[k]*tasks[k]['period'] - Rss1 - task['Sseg'][0])
        
    # compute the response time of tau_{n,2}:
    Rss2 = wcrt(task['Cseg'][1], tasks, offset)
    Rss = Rss1 + Rss2 + task['Sseg'][0]
    
    if Rss < UBss and Rss2 < UBss2:
        for k in range(n):
            if NI[k] > 0:
                NIp = list(NI)
                NIp[k] = NIp[k] - 1

                R = RespTime(tasks, task, offset, NIp, syn, processedNI)
                if R > Rss:
                    Rss = R    
    return Rss


# Input: Segments that can be refined, Taskset
# Output: Index of task that should be refined
def selectToRefine(sync, tasks):
    imax = 0
    for i in range(len(sync)):
        if sync[i] == 12:
            imax = i
            break
    for i in range(len(sync)):
        if sync[i] == 12 and tasks[i]["utilization"] > tasks[imax]["utilization"]:
            imax = i
    return imax


# Input: Segment
# Output: Can the segment be abstracted
def isAbst(head):
    if 12 in head:
        return True
    return False

# Input: Taskset, execution time, task-offsets
# Output: Maximum number of execution times of each task during interval
def maxRels(tasks,execution,offset):
    rt = wcrt(execution,tasks,offset) + 0.0
    NI = []
    for task in tasks:
        NI.append( math.ceil(rt / task['period']) )
    return NI


# Input: Execution time, taskset, task-offsets
# Output: worst-case-response-time of task
def wcrt(execution, tasks,offset):
    Wn = execution
    loads = [rf(Wn,task['period'],sum(tasks[u]['Cseg'])+task["sslength"],offset[u]) for u,task in enumerate(tasks)]
    t = execution + sum(loads)
    while(t > Wn):
        Wn = t
        loads = [rf(Wn,task['period'],sum(tasks[u]['Cseg'])+task["sslength"],offset[u]) for u,task in enumerate(tasks)]
        t = execution + sum(loads)
    return t

# Input: time, period, execution time, offset
# Output: response-time of task
def rf(t,T,E,O):
    return math.ceil((t-O + 0.0) / T) * E 
