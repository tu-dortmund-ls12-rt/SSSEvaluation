import math
import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Generalized multiframe mode schedulability test with parameter adaptation as milp-epsilon
# From: https://link.springer.com/article/10.1007/s11241-017-9279-2
# Input: Task set
# Output: Schedulability of the Task Set under GMFPA
def GMFPA(tasks,ischeme):
    #tasks = [{'period': 865, 'execution': 5, 'deadline': 865, 'utilization': 0.005975544927920393, 'sslength': 60, 'minSr': 1, 'paths': [{'Cseg': [1, 4], 'Sseg': [58], 'deadline': [-1, -1]}, {'Cseg': [1, 4], 'Sseg': [60], 'deadline': [-1, -1]}], 'Cseg': [1, 4], 'Sseg': [60]}, {'period': 2024, 'execution': 88, 'deadline': 2024, 'utilization': 0.04402445507207961, 'sslength': 43, 'minSr': 1, 'paths': [{'Cseg': [6, 82], 'Sseg': [43], 'deadline': [-1, -1]}, {'Cseg': [8, 64], 'Sseg': [40], 'deadline': [-1, -1]}], 'Cseg': [8, 82], 'Sseg': [43]}]
    #tasks = [{'period': 711, 'execution': 96, 'deadline': 711, 'utilization': 0.13612793259110334, 'sslength': 59, 'minSr': 1, 'paths': [{'Cseg': [44, 52], 'Sseg': [54], 'deadline': [-1, -1]}, {'Cseg': [40, 39], 'Sseg': [59], 'deadline': [-1, -1]}], 'Cseg': [44, 52], 'Sseg': [59]}, {'period': 817, 'execution': 522, 'deadline': 817, 'utilization': 0.64019865591712, 'sslength': 19, 'minSr': 1, 'paths': [{'Cseg': [3, 519], 'Sseg': [19], 'deadline': [-1, -1]}, {'Cseg': [421, 61], 'Sseg': [16], 'deadline': [-1, -1]}], 'Cseg': [421, 519], 'Sseg': [19]}, {'period': 4269, 'execution': 100, 'deadline': 4269, 'utilization': 0.023673411491776708, 'sslength': 88, 'minSr': 1, 'paths': [{'Cseg': [1, 96], 'Sseg': [86], 'deadline': [-1, -1]}, {'Cseg': [11, 89], 'Sseg': [88], 'deadline': [-1, -1]}], 'Cseg': [11, 96], 'Sseg': [88]}]

    #Calculate n and N_i
    len_tasks = len(tasks)
    len_segs = 2*len(tasks[0]['Cseg'])-1

    #Calculate U_cap
    U_cap = 0
    for i in range(len_tasks):
        U_cap += tasks[i]['utilization']

    #Calculate H
    P_max = 0
    for i in range(len_tasks):
        task = tasks[i]
        if(task['period']-min(task['Cseg']) > P_max):
            P_max = task['period']-min(task['Cseg'])

    H = 0
    if U_cap < 1:
        H = math.ceil(U_cap/(1-U_cap) * P_max)
    else:
        periods = list(range(len_tasks))
        for i in range(len_tasks):
            periods[i] = tasks[i]['period']
        #print(periods)
        H = np.lcm(periods)

    #Approximation of H to Ha

    epsilon = 1+(float)(ischeme.split('-')[1])
    len_Ha = math.ceil(math.log(H,epsilon))+1

    Ha = list(range(len_Ha))
    for i in range(len_Ha):
        Ha[i] = 1*math.pow(epsilon,i)
    Ha[len_Ha-1]=H

    #Calculate realmin
    realmin = np.finfo(float).tiny
    
    #Set Constants
    Pi = list(range(len_tasks))
    Eik = list(range(len_tasks))
    Di = list(range(len_tasks))

    for i in range(len_tasks):
        Pi[i] = tasks[i]['period']
        Di[i] = tasks[i]['deadline']
        Eik[i] = list(range(len_segs))
        for k in range(len_segs):
            if k%2 == 0:
                Eik[i][k] = tasks[i]['Cseg'][int(k/2)]
            else:
                Eik[i][k] = 0

    # print("Tasks: ",tasks)
    # print("Number of tasks n: ",len_tasks)
    # print("Number of Segments Ni: ",len_segs)
    # print("Utilization: ",U_cap)
    # print("P_max: ",P_max)
    # print("H: ",H)
    # print("Epsilon: ",epsilon)
    # print("len_Ha: ",len_Ha)
    # print("Ha ",Ha)
    # print("realmin: ",realmin)
    # print("Pi: ",Pi)
    # print("Di: ",Di)
    # print("Eik: ",Eik)

    #Create Gurobi Model
    m = gp.Model("mip1")

    #Set Variables
    Dik = m.addMVar(    (len_tasks,len_segs)                    ,vtype=GRB.CONTINUOUS   ,name="Dik")
    # Pik = m.addMVar(    (len_tasks,len_segs)                   ,vtype=GRB.CONTINUOUS   ,name="Pik") # implicit deadline, not needed
    Tb = m.addMVar(     (len_tasks,len_Ha,len_segs,len_segs) ,vtype=GRB.CONTINUOUS   ,name="Tb")
    Xitjk = m.addMVar(  (len_tasks,len_Ha,len_segs,len_segs) ,vtype=GRB.BINARY       ,name="Xitjk")
    Yitjk = m.addMVar(  (len_tasks,len_Ha,len_segs,len_segs) ,vtype=GRB.CONTINUOUS   ,name="Yitjk")
    Yitj = m.addMVar(   (len_tasks,len_Ha,len_segs)          ,vtype=GRB.CONTINUOUS   ,name="Yitj")
    Yit = m.addMVar(    (len_tasks,len_Ha)                   ,vtype=GRB.CONTINUOUS   ,name="Yit")
    L = m.addMVar(      (1)                                     ,vtype=GRB.CONTINUOUS   ,name="L")

    
    m.setObjective(L, GRB.MINIMIZE)
    # Condition 1-6
    m.addConstrs((Eik[i][k] <= Dik[i,k] 
                            for i in range(len_tasks)
                            for k in range(len_segs)),name='c1')
                            
    m.addConstrs((Dik[i,:].sum() <= Pi[i] 
                            for i in range(len_tasks)),name='c2')
    # Condition 7           
    m.addConstrs((Yitjk[i,t,j,k] == Xitjk[i,t,j,k] * Eik[i][k] + math.floor(Ha[t]/Pi[i])*Eik[i][k] 
                            for t in range(len_Ha)
                            for i in range(len_tasks)
                            for j in range(len_segs)
                            for k in range(len_segs)),name='c7')
    # Condition 8
    m.addConstrs(((Ha[t]-Tb[i,t,k,j])/Pi[i] <= Xitjk[i,t,j,k] - realmin/Pi[i]
                            for t in range(len_Ha)
                            for i in range(len_tasks)
                            for j in range(len_segs)
                            for k in range(len_segs)),name='c8')
    # Condition 9
    m.addConstrs((Tb[i,t,k,j] == Dik[i,j:k].sum()+Dik[i,k]+math.floor(Ha[t]/Pi[i])*Pi[i]
                            for t in range(len_Ha)
                            for i in range(len_tasks)
                            for j in range(len_segs)
                            for k in range(len_segs)),name='c9')

    # Condition 10
    m.addConstrs((Yitj[i,t,j] == Yitjk[i,t,j,:].sum()
                            for t in range(len_Ha)
                            for i in range(len_tasks)
                            for j in range(len_segs)),name='c10')
    # Condition 11
    m.addConstrs((Yit[i,:] >= Yitj[i,:,j]
                            #for t in range(len_Ha)
                            for i in range(len_tasks)
                            for j in range(len_segs)),name='c11')
    # Condition 12
    m.addConstrs((Yit[:,t].sum() <= L*Ha[t]
                            for t in range(len_Ha)),name='c12')


    # Suspension times equal to deadlines of suspensing frames
    m.addConstrs((Dik[i,k] == tasks[i]['Sseg'][int((k-1)/2)]
                            for i in range(len_tasks)
                            for k in range(1,len_segs,2)),name='c13')

    #Start Optimizer
    m.setParam( 'OutputFlag', False )
    m.update()
    m.optimize()
    if m.Status==2:
        # Print all Variables
        # for v in m.getVars():
        #     print('%s %g' % (v.varName, v.x))
        # print('Obj: %g' % m.objVal)

        dbf = [0] * len_Ha

        for t in range(len_Ha):
            for i in range(len_tasks):
                dbf[t] += Yit.x[i,t]
            #print("DBF ",dbf[t])
            #print("SBF ",Ha[t])
            if dbf[t] > Ha[t]:
                #print("Return False")
                return False
        #print("Return True")
        return True
    else:
        m.computeIIS()
        m.write("gmfpa.ilp") 
        return False
            


    

# GMFPA([],"GMFPA-0.5")


