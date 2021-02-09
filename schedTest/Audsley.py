from schedTest import PASS
def Audsley(tasks):
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
			#print "all :",tasks
			#print "task:",itask
			#print "prime:",primeTasks
			#print ""

			
			Tn=itask['period']
			maxSC=0
			for j in range(len(itask["paths"])):
				SC=0
				for k in range(len(itask["paths"][j]['Cseg'])):
					SC+=itask["paths"][j]['Cseg'][k]
				for k in range(len(itask["paths"][j]['Sseg'])):
					SC+=itask["paths"][j]['Sseg'][k]
				maxSC=max(maxSC,SC)
				

			if PASS.PASS(maxSC,Tn,primeTasks) == True:
				priortyassigned[i]=1
				canLevel=1
				tasks[i]['priority']=len(tasks)-plevel
				break	
		if canLevel == 0:
			#print "fail assign at",plevel 
			return False 
	#print tasks
	return True