import math
import gurobipy as gp
from gurobipy import GRB
import numpy as np


# WCRT-Approximation by task interference applied on Real-Time Applications on Dynamic Reconfigurable FPGAs
# From: https://ieeexplore.ieee.org/document/7176028 and https://ieeexplore.ieee.org/document/7809838
# Input: Task set
# Output: Schedulability of the Task Set
def Milpreleasejitter(tasks):
	len_tasks = len(tasks)
	#wcrt of each task
	wcrt = [0] * len_tasks
	for i in range(len_tasks):
		#Get higher priority tasks and current task tss
		hp_tasks = tasks[0:i]
		tss = tasks[i]

		#Variables for loops
		len_hp_tasks = len(hp_tasks)
		len_c_segs = len(tss['Cseg'])

		#Variables for Task tss and higher priority tasks
		c_segs = tss['Cseg']
		s_segs = tss['Sseg']
		Cj = [task['execution'] for task in hp_tasks]
		Tj = [task['period'] for task in hp_tasks]
		Jk = [wcrt[j]-Cj[j] for j in range(len_hp_tasks)]

		#Determine upper bound for task
		UBss = 0
		t = 0
		t = sum(tss['Cseg'])+sum(tss['Sseg'])+sum([math.ceil((t+Jk[p])/Tj[p])*Cj[p] for p in range(len_hp_tasks)])
		while UBss != t:
			UBss = t
			t = sum(tss['Cseg'])+sum(tss['Sseg'])+sum([math.ceil((t+Jk[p])/Tj[p])*Cj[p] for p in range(len_hp_tasks)])

		#Determine upper bound for computation segments
		UBssj = [0] * len_c_segs
		for j in range(len_c_segs):
			t = 0
			t = tss['Cseg'][j]+sum([math.ceil((t+Jk[p])/Tj[p])*Cj[p] for p in range(len_hp_tasks)])
			while UBssj[j] != t:
				UBssj[j] = t
				t = tss['Cseg'][j]+sum([math.ceil((t+Jk[p])/Tj[p])*Cj[p] for p in range(len_hp_tasks)])

		#Create model
		m = gp.Model("mip1")

		#Accuracy for ceil or floor
		IntFeasTol = 1e-4

		#Define variables
		Rssj = m.addMVar((len_c_segs) ,vtype=GRB.CONTINUOUS   ,name="Rssj")
		NikjCont = m.addMVar((len_hp_tasks,len_c_segs) ,vtype=GRB.CONTINUOUS   ,name="NikjCont")
		NikjCeil = m.addMVar((len_hp_tasks,len_c_segs) ,vtype=GRB.INTEGER   ,name="NikjCeil")
		Nikj = m.addMVar((len_hp_tasks,len_c_segs) ,vtype=GRB.INTEGER   ,name="Nikj")
		Okj = m.addMVar((len_hp_tasks,len_c_segs) ,vtype=GRB.CONTINUOUS   ,name="Okj")
		relkj = m.addMVar((len_hp_tasks,len_c_segs) , vtype=GRB.CONTINUOUS   ,name="relkj")
		dpj = m.addMVar((len_hp_tasks,len_c_segs) ,vtype=GRB.CONTINUOUS   ,name="dpj")
		divpkj = m.addMVar((len_hp_tasks,len_hp_tasks,len_c_segs) ,vtype=GRB.CONTINUOUS   ,name="divpkj")
		floorpkj = m.addMVar((len_hp_tasks,len_hp_tasks,len_c_segs) ,vtype=GRB.INTEGER   ,name="floorpkj")
		sumpkj = m.addMVar((len_hp_tasks,len_hp_tasks,len_c_segs) ,vtype=GRB.CONTINUOUS   ,name="sumpkj")
		sumkj = m.addMVar((len_hp_tasks,len_c_segs) ,vtype=GRB.CONTINUOUS   ,name="sumkj")

		#Set lower bounds of variables for constraints 8-10
		relkj.LB = -GRB.INFINITY
		dpj.LB = -GRB.INFINITY
		divpkj.LB = -GRB.INFINITY
		floorpkj.LB = -GRB.INFINITY
		sumpkj.LB = -GRB.INFINITY
		sumkj.LB = -GRB.INFINITY

		#Maximize sum of Response Times
		m.setObjective(sum(Rssj), GRB.MAXIMIZE)

		#Constraint 1
		m.addConstr((Rssj[:].sum() + sum(s_segs) <= UBss ),name='c1')

		#Constraint 2
		m.addConstrs((Rssj[j] == c_segs[j] + sum(i[0] * i[1] for i in zip(Nikj[:,j], Cj))
					for j in range(len_c_segs)),name='c2')

		#Constraint 3
		m.addConstrs((Rssj[j] <= UBssj[j]
					for j in range(len_c_segs)),name='c3')

		#Constraint 4
		m.addConstrs((Okj[k,j] >= -Jk[k]
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c4')

		#Constraint 5
		m.addConstrs(((Okj[k,j+1] >=  Okj[k,j] + Nikj[k,j]*Tj[k] - (Rssj[j] + s_segs[j]) - Jk[k])
					for k in range(len_hp_tasks)
					for j in range(len_c_segs-1)),name='c5')

		#Constraint 6
		m.addConstrs((Nikj[k,j] >= 0
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c6')

		m.addConstrs((NikjCont[k,j] >= 0
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c6cont')

		m.addConstrs((NikjCeil[k,j] >= 0
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c6ceil')

		#Constraint 7
		m.addConstrs((NikjCont[k,j] == (Rssj[j]-Okj[k,j])/Tj[k]
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c7cont')

		m.addConstrs((NikjCeil[k,j] >= NikjCont[k,j]
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c7ceil1')

		m.addConstrs((NikjCeil[k,j]-1 <= NikjCont[k,j]-IntFeasTol
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c7ceil2')

		m.addConstrs((Nikj[k,j] <= NikjCeil[k,j]
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c7')

		# Constraint 8
		m.addConstrs((divpkj[p,k,j] == (dpj[p,j]-relkj[k,j])/Tj[p]
					for p in range(len_hp_tasks)
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c8div')

		m.addConstrs((floorpkj[p,k,j] <= divpkj[p,k,j]
					for p in range(len_hp_tasks)
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c8floor1')

		m.addConstrs((floorpkj[p,k,j]+1 >= divpkj[p,k,j]+IntFeasTol
					for p in range(len_hp_tasks)
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c8floor2')

		m.addConstrs((sumpkj[p,k,j] >= floorpkj[p,k,j]*Cj[p]
					for p in range(len_hp_tasks)
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c8sumparts1')

		m.addConstrs((sumpkj[p,k,j] >= 0
					for p in range(len_hp_tasks)
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c8sumparts2')

		m.addConstrs((sumkj[k,j] == sumpkj[:,k,j].sum()
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c8sum')

		m.addConstrs((Rssj[j] >= relkj[k,j] + sumkj[k,j] + IntFeasTol
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c8')

		# Constraint 9
		m.addConstrs((relkj[k,j] == Okj[k,j] + (Nikj[k,j]-1) * Tj[k]
					for k in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c9')

		# Constraint 10
		m.addConstrs((dpj[p,j] == Okj[p,j] + Nikj[p,j] * Tj[p]
					for p in range(len_hp_tasks)
					for j in range(len_c_segs)),name='c10')

		#Update and optimize model
		m.update()
		m.optimize()
		if m.Status==2:
			# Print all Variables
			# for v in m.getVars():
			#     print('%s %g' % (v.varName, v.x))
			#print('Obj: %g' % m.objVal)

			#Set WCRT of current task tss
			wcrt[i] = m.objVal + sum(tss['Sseg'])
			#If the wcrt is higher than the period, the task set is unschedulable
			if wcrt[i] > tss['period']:
				return False
			#print("Return True")
		else:
			# MILP is unfeasible and task set cant be scheduled
			m.computeIIS()
			m.write("Milpreleasejitter.ilp")
			return False
	#Everything is schedulable
	return True
