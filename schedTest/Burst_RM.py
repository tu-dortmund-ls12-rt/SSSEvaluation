from schedTest import SEIFDA
import numpy

def BURST_RM(tasks):
	#sorting tasks by increasing period
	sortedTasksRM=sorted(tasks, key=lambda item:item['period']) 
	#print sortedTasksLM
	for i in range(len(sortedTasksRM)):
		HPTasks=sortedTasksRM[:i]
		#print HPTasks
		Cn=sortedTasksRM[i]['execution']
		Sn=sortedTasksRM[i]['sslength']
		Tn=sortedTasksRM[i]['period']
		if Burst_HP(Cn,Sn,Tn,sortedTasksRM[:i])==False:
				return False
				
def Burst_HP(Cn,Sn,Tn,HPTasks):
	Tasks=[]
	for itask in HPTasks:	
		Tasks.append(itask)

	for itask in Tasks:	
		alpha=1+(1/int(Tn/itask['period']))
		itask['alpha']=alpha
	#sorting by increasing alpha
	sortedTasksAlpha=sorted(Tasks, key=lambda item:item['alpha']) 
	sumL=0
	for i in range(len(sortedTasksAlpha)):
		prod=1
		for j in range(i,len(sortedTasksAlpha)):
			prod*(1+sortedTasksAlpha[j]['execution']/sortedTasksAlpha[j]['period'])

		sumL+=(sortedTasksAlpha[i]['alpha']+1)*(sortedTasksAlpha[i]['execution']/sortedTasksAlpha[i]['period'])/prod
	if (Cn+Sn)/Tn <= 1-sumL:
		return True
	else:
		return False