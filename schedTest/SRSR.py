import math

def SRSR(tasks):
    #tasks = [{'period': 865, 'execution': 5, 'deadline': 865, 'utilization': 0.005975544927920393, 'sslength': 60, 'minSr': 1, 'paths': [{'Cseg': [1, 4], 'Sseg': [58], 'deadline': [-1, -1]}, {'Cseg': [1, 4], 'Sseg': [60], 'deadline': [-1, -1]}], 'Cseg': [1, 4], 'Sseg': [60]}, {'period': 2024, 'execution': 88, 'deadline': 2024, 'utilization': 0.04402445507207961, 'sslength': 43, 'minSr': 1, 'paths': [{'Cseg': [6, 82], 'Sseg': [43], 'deadline': [-1, -1]}, {'Cseg': [8, 64], 'Sseg': [40], 'deadline': [-1, -1]}], 'Cseg': [8, 82], 'Sseg': [43]}]
    tasks = [{'period': 711, 'execution': 96, 'deadline': 711, 'utilization': 0.13612793259110334, 'sslength': 59, 'minSr': 1, 'paths': [{'Cseg': [44, 52], 'Sseg': [54], 'deadline': [-1, -1]}, {'Cseg': [40, 39], 'Sseg': [59], 'deadline': [-1, -1]}], 'Cseg': [44, 52], 'Sseg': [59]}, {'period': 817, 'execution': 522, 'deadline': 817, 'utilization': 0.64019865591712, 'sslength': 19, 'minSr': 1, 'paths': [{'Cseg': [3, 519], 'Sseg': [19], 'deadline': [-1, -1]}, {'Cseg': [421, 61], 'Sseg': [16], 'deadline': [-1, -1]}], 'Cseg': [421, 519], 'Sseg': [19]}, {'period': 4269, 'execution': 100, 'deadline': 4269, 'utilization': 0.023673411491776708, 'sslength': 88, 'minSr': 1, 'paths': [{'Cseg': [1, 96], 'Sseg': [86], 'deadline': [-1, -1]}, {'Cseg': [11, 89], 'Sseg': [88], 'deadline': [-1, -1]}], 'Cseg': [11, 96], 'Sseg': [88]}]

    print(tasks)

    len_tasks = len(tasks)
    len_segs = 2*len(tasks[0]['Cseg'])-1

    print("len_tasks: ",len_tasks)
    print("len_segs: ",len_segs)

    for i in range(len_tasks):
        SRSR_n(tasks,i)


    return False

def SRSR_n(tasks,n):
    #Create stack
    store = []
    print("n: ",n)

    #Create A for sync list
    len_c_segs = len(tasks[0]['Cseg'])
    A = list(range(n))
    for i in range(n):
        A[i]=list(range(len_c_segs))
    print(A)

    #Add A to stack
    store.append(A)

    #Calculate maximum number of interfering jobs
    Nup = list(range(n))
    for i in range(n):
        print("period: ",tasks[i]['period'])
        Nup[i] = math.ceil(WCRT_SRSR(tasks,n)/tasks[i]['period'])
    print("Nup: ", Nup)

    #Deadline for TDA analysis
    Dn = tasks[n]['deadline']

    #While the Stack is not empty, process each element
    while store:
        A = store.pop()
        print("A: ",A)
        #Calculate the reponse time 
        if RT_SRSR(tasks,n,A,Nup) > Dn:
            abstract = False
            for i in range(len(A)):
                if len(A[i])>1:
                    abstract = True
            if abstract:
                Ai = [0]*len(A)
                print("Ai: ",Ai)
                for i in range(len(A)):
                    Ai[i]=A[:]
                print("Ai: ",Ai)
                imax = 0
                for i in range(len(A)):
                    if len(A[i])>1 and tasks[i]["utilization"] > tasks[imax]["utilization"]:
                        imax = i
                print("imax: ",imax)
                for i in range(len(A)):
                    Ai[i][imax] = [i]
                    store.append(Ai[i])
                print("Ai: ",Ai)
                print("store: ",store)
            else:
                return False
    return True

def WCRT_SRSR(tasks,n):
    print("n2: ",n)
    Ci = list(range(n))
    Cn = tasks[n]['Cseg'][0]
    Ti = list(range(n))
    Dn = tasks[n]['deadline']
    len_c_segs = len(tasks[0]['Cseg'])
    len_s_segs = len(tasks[0]['Sseg'])

    for i in range(n):
        Ti[i] = tasks[i]['deadline']
        print(tasks[i])
        for c in range(len_c_segs):
            Ci[i]+= tasks[i]['Cseg'][c]
        for s in range(len_s_segs):
            Ci[i]+= tasks[i]['Sseg'][s]
    print("Ci: ",Ci)
    print("Cn: ",Cn)
    print("Ti: ",Ti)
    print("Dn: ",Dn)
    
    Wn = Cn
    t = sum(Ci)
    while t > Wn:
        Wn = Cn
        for i in range(n):
            Wn += math.ceil(t/Ti[i])*Ci[i]
            Wn += Ci[i]
        if t > Dn:
            break
        t = Wn

    print("t: ",t)
    print("Wn: ",Wn)

    return t


def RT_SRSR(tasks,n,Syn,Nup):
    N = Nup[:]


    len_c_segs = len(tasks[0]['Cseg'])
    len_s_segs = len(tasks[0]['Sseg'])
    Ci = list(range(n))
    for i in range(n):
        print(tasks[i])
        for c in range(len_c_segs):
            Ci[i]+= tasks[i]['Cseg'][c]
        for s in range(len_s_segs):
            Ci[i]+= tasks[i]['Sseg'][s]

    Rss1b = 0
    Rss1 = tasks[n]['Cseg'][0]
    for i in range(n):
        Rss1 += Nup[i]*Ci[i]
    while Rss1b != Rss1:
        Rss1b = Rss1
        for i in range(n):
            if Syn[i]==[2] and N[i] > (Rss1+tasks[n]['Sseg'][0])/tasks[i]['period']:
                N[i] = N[i]-1
        Rss1 = tasks[n]['Cseg'][0]
        for i in range(n):
            Rss1 += min(N[i],math.ceil(Rss1/tasks[i]['period']))*Ci[i]
        
        for i in range(n):
            N[i] = min(N[i],math.ceil(Rss1/tasks[i]['period']))
    
    O = list(range(n))
    for i in range(n):
        if Syn[i] == [0,1]:
            O[i] = 0
        else:
            O[i] = max(0,N[i]*tasks[i]['period']-Rss1-tasks[n]['Sseg'][0])
    Rss2 = tasks[n]['Cseg'][1]
    for i in range(n):
        Rss2 += math.ceil((Rss2-O[i])/tasks[i]['period'])*Ci[i]
    Rss = Rss1 + tasks[n]['Sseg'][0]+Rss2
    
    

    return 1

#SRSR([])
