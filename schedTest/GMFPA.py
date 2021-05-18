import math
import gurobipy as gp
from gurobipy import GRB
import numpy as np

# Generalized multiframe mode schedulability test with parameter adaptation as milp-epsilon
# From: https://link.springer.com/article/10.1007/s11241-017-9279-2
# Input: Task set
# Output: Schedulability of the Task Set under GMFPA
def GMFPA(tasks,ischeme):
    #Calculate n and N_i
    len_tasks = len(tasks)
    len_segs = 2*len(tasks[0]['Cseg'])-1y

    #Calculate U_cap
    U_cap = sum([task['utilization'] for task in tasks])

    #Calculate H
    P_max = max([task['period']-min(task['Cseg']) for task in tasks])

    H = 0
    if U_cap < 1:
        H = math.ceil(U_cap/(1-U_cap) * P_max)
    else:
        periods = [task['period'] for task in tasks]
        #print(periods)
        H = np.lcm(periods)


    #Approximation of H to Ha
    Ha = []
    len_Ha = 0
    epsilon = 1+(float)(ischeme.split('-')[1])
    if epsilon != 1:
        len_Ha = math.ceil(math.log(H,epsilon))+1
        Ha = [1*math.pow(epsilon,i) for i in range(len_Ha)]
        Ha[len_Ha-1] = H
    else:
        len_Ha = H
        Ha = list(range(H))

    #Calculate realmin
    realmin = np.finfo(float).tiny
    
    #Set Constants
    Pi = [task['period'] for task in tasks]
    Eik = [[tasks[i]['Cseg'][int(k/2)] if k%2 == 0 else 0 for k in range(len_segs)] for i in range(len_tasks)]

    #print("Tasks: ",tasks)
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

GMFPA([],'GMFPA-1')

