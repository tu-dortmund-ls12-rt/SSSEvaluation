from schedTest import rad
import sys

def PASS_OPA(tasks,scheme):
	#Optimal Priority Assignment
	priortyassigned=[0 for i in range(len(tasks))]
	for plevel in range(len(tasks)):
		canLevel=0
		## check whether task i can be assigned with the priority level plevel
		for i in range(len(tasks)):
			##ignore lower priority tasks
			if priortyassigned[i]==1:
				continue
			itask=tasks[i]

			## get higher prioirty tasks
			primeTasks=[]
			for j in range(len(tasks)):
				if priortyassigned[j]==0 and i != j:
					primeTasks.append(tasks[j])


			Tn=itask['period']
			Cn=itask['execution']
			Sn=itask['sslength']
			D=(itask['deadline']-itask['sslength'])/len(itask['Cseg'])
			maxSC=0
			for j in range(len(itask["paths"])):
				SC=0
				for k in range(len(itask["paths"][j]['Cseg'])):
					SC+=itask["paths"][j]['Cseg'][k]
				for k in range(len(itask["paths"][j]['Sseg'])):
					SC+=itask["paths"][j]['Sseg'][k]
				maxSC=max(maxSC,SC)
			if scheme == "PASS-OPA":
				if rad.PASS(maxSC,Tn,primeTasks) == True:
					priortyassigned[i]=1
					canLevel=1
					tasks[i]['priority']=len(tasks)-plevel
					break
			elif scheme == "SCAIR-OPA":
				if (rad.segTest(Cn,Sn,Tn,primeTasks) or rad.SUMTest(itask,primeTasks) )==True:
					priortyassigned[i]=1
					canLevel=1
					tasks[i]['priority']=len(tasks)-plevel
					break
			elif scheme == "EDAGMF-OPA":
				if rad.EDAGMF(itask,primeTasks,D)==True:
					priortyassigned[i]=1
					canLevel=1
					tasks[i]['priority']=len(tasks)-plevel
					break
			else:
				sys.exit(2)
		if canLevel == 0:
			return False
	return True
