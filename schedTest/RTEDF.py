# FROM https://ieeexplore.ieee.org/abstract/document/9211430 Algorithm 1
import math # math.ceil(), math.floor()
import time

# Sorts task list by period length
# Input: Task set
# Output: Sorted task set by period
def sort_by_period(tasks): 
    return sorted(tasks, key=lambda k: k['period'])

# Calls RTEDF
# Input: Task set
# Output: Schedulability under RTEDF
def RTEDF(tasks):
    return RTEDF_with_improv(tasks)

# Calls RTEDF
# Input: Task set
# Output: Schedulability under RTEDF
def RTEDF_wo_improv(tasks):
    htasks = sort_by_period(tasks)
    n = len(htasks)
    Rtilde = [0]*n
    for k in reversed(range(n)):
        Atilde=[0]*n # Compute Atilde_i^k for all i
        for i in range(n):
            if i != k:
                Tk = htasks[k]['period']
                Ti = htasks[i]['period']
                Ck = htasks[k]['execution']
                Sk = htasks[k]['sslength']

                if i<k:
                    Atilde[i] = Tk - math.floor(Tk/Ti) * Ti
                if i>k:
                    Atilde[i] = Tk + Rtilde[i] - (math.floor(Tk/Ti) +1)*Ti

        # print('Atilde')
        # print(Atilde)

        Rtildek = [0]*(n) # Compute Rtilde_k(j) for all j
        for j in range(n):
            if j == k: # this is the j==0 case
                R=0
                R += Ck+Sk
                for ji in range(n):
                    if ji != k:
                        R += math.floor(htasks[k]['period']/htasks[ji]['period'])*htasks[ji]['execution']
                for ji in range(n):
                    if ji != k:
                        R += htasks[ji]['execution']
                Rtildek[j] = R
            else:
                R=0
                R += Ck+Sk
                for ji in range(n):
                    if ji != k:
                        R += math.floor(htasks[k]['period']/htasks[ji]['period'])*htasks[ji]['execution']
                for ji in range(n):
                    if ji != k and Atilde[ji] > Atilde[j]:
                        R += htasks[ji]['execution']
                R+= max(Atilde[j],0)
                Rtildek[j] = R

        Rtilde[k] = min(Rtildek)
        # print('Rtilde')
        # print(Rtilde)
        if Rtilde[k] > htasks[k]['period']:
            return False
    return True

# Calls RTEDF
# Input: Task set
# Output: Schedulability under RTEDF
def RTEDF_with_improv(tasks):
    htasks = sort_by_period(tasks)
    n = len(htasks)
    Rtilde = [0]*n
    for k in reversed(range(n)):
        ik = list(range(n))
        ik.remove(k)

        Tk = htasks[k]['period']
        Ck = htasks[k]['execution']
        Sk = htasks[k]['sslength']

        Atildek=[0]*n # Compute Atilde_i^k for all i

        for i in ik:
            Ti = htasks[i]['period']

            if i<k:
                Atildek[i] = Tk - math.floor(Tk/Ti) * Ti
            if i>k:
                Atildek[i] = Tk + Rtilde[i] - (math.floor(Tk/Ti) +1.0)*Ti

        # print('Atildek')
        # print(Atildek)

        Rtildek = [0]*(n) # Compute Rtilde_k(j) for all j

        R = Ck+Sk
        for i in ik:
            R += (math.floor(Tk/htasks[i]['period'])+1)*htasks[i]['execution']
        Rtildek[k] = R


        for j in ik:
            mjk = max(Atildek[j],0.0)
            ijk = [i for i in ik if Atildek[i] <= Atildek[j]]

            R = 0.0
            for i in ik:
                if i not in ijk:
                    R += min(math.floor(htasks[k]['period']/htasks[i]['period'])+1.0, math.ceil((htasks[k]['period'] - mjk)/htasks[i]['period']))*htasks[i]['execution']
                else:
                    R += min(math.floor(htasks[k]['period']/htasks[i]['period']), math.ceil((htasks[k]['period'] - mjk)/htasks[i]['period']))*htasks[i]['execution']
            R += Ck + Sk + mjk
            Rtildek[j] = R

        Rtilde[k] = min(Rtildek)
        # print('Rtilde')
        # print(Rtilde)
        if Rtilde[k] > htasks[k]['period']:
            return False
    return True
