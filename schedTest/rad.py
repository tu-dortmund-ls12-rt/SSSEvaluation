from __future__ import division
import random
import math
import json
import sys, getopt

# from ssuspension import sortedTasks

maxmaxP=[]
rfile=""

selectUT=""
mProc=1
Cn=1
def parameterRead():
	global rfile,selectUT,selectUT,mProc
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:s:m:")
	except getopt.GetoptError:
		print 'test.py -i <seed> -u <totalutilzation> -if <scalefactor>'
		sys.exit(2)
	print opts, args
	
	for opt, arg in opts:
		if opt == '-h':
			print 'test.py -s <randoseed> -u <totalutilzation> -f <scalefactor>'
			sys.exit()		
		elif opt in ("-i", "--input"):
			rfile = arg
		elif opt in ("-s", "--select"):
			selectUT = arg
		elif opt in ("-m", "--proc"):
			mProc = int(arg)
		else:
			assert False, "unhandled option"
def maxU_cmp(x):
	return x['execution']/x['period']
		


def highPTaskDemand(R,tasks):
	sumDM=0
	for itask in tasks:
		sumDM+=itask['execution']*math.ceil(R/itask['period'])
	return sumDM

def NCDemandBurst(t,tasks):
	sumDM=0
	for itask in tasks:		
		D=itask['execution']*math.ceil((t+itask['sslength'])/itask['period'])
		sumDM+=D
	return sumDM
def highDemandBurst(t,tasks):
	sumDM=0
	for itask in tasks:		
		if itask['sslength']!=0:
			D=itask['execution']*math.ceil((t)/itask['period'])	+itask['execution']	
		else:
			D=itask['execution']*math.ceil((t)/itask['period'])	
		sumDM+=D
	return sumDM
def sssNCDT(Cn,Sn,Tn,HPTasks):	
	R=0
	while True:		
		dm=NCDemandBurst(R,HPTasks)
		if dm+Cn+Sn> Tn:
			return False

		if R != dm+Cn+Sn:
			R=dm+Cn+Sn			
		else: 
			if R> Tn:
				return False
			else:
				return True
def BlkhighPTaskDemand(R,tasks):
	sumDM=0
	for itask in tasks:
		sumDM+=itask['execution']*math.ceil((R+itask['blocking'])/itask['period'])
	return sumDM
def ssBlkTA(Sn,tasks):
	if Sn==0:
		return 0
	R=0
	while True:		
		dm=BlkhighPTaskDemand(R,tasks)

		if R != dm+Sn:
			R=dm+Sn			
		else: 
			return R

def sssBlkDT(Cn,Sn,Tn,HPTasks):
	
	R=0
	while True:		
		dm=BlkhighPTaskDemand(R,HPTasks)
		if dm+Cn+Sn> Tn:
			return False
		if R != dm+Sn+Cn:
			R=dm+Sn+Cn			
		else: 
			if R> Tn:
				return False
			else:
				return True
def alpha_t(t,itask,i):

	l=i

	sumT=0
	numcseg=len(itask["Cseg"])
	while 1:

		if l%numcseg!=numcseg-1:
			sumT+=itask["Cseg"][l%numcseg]+itask["Sseg"][l%numcseg]*itask['minSr']
		else:
			if l <=numcseg:
				sumT+=itask["Cseg"][numcseg-1]+itask["period"]-itask["period"]
			else:
				sumT+=itask["Cseg"][numcseg-1]+(itask["period"]-(itask["execution"]+itask["sslength"]*itask['minSr']))
		if sumT>= t:
			break
		else:
			l+=1
	return l
def MRBF(t,itask):
	
	maxD=0
	numcseg=len(itask['Cseg'])
	for i in range(numcseg):
		D=0
		
		jump=int(t/itask['period'])
		tjump=t
		if jump >= 2:
			tjump=t-(jump-2)*itask['period']
			D+=(jump-2)*itask['execution']
		else:
			tjump=t
		l=alpha_t(tjump,itask,i)	
		#print "tjump:",tjump,"l:",l
		for j in range(i,l+1):			
			D+=itask["Cseg"][j%numcseg]			

		if D > maxD:
			maxD=D
	#print "t: ",t,"d:",maxD,itask
	return maxD
def ssRTA(Cn,HPTasks,Tn):
	R=0
	while True:	

		dm=0
		for itask in HPTasks:
			if itask['sslength']==0:
				dm+=itask['execution']*math.ceil((R)/itask['period'])	
			else:
				dm+=MRBF(R,itask)
		
		if dm+Cn> Tn:
			return dm+Cn

		if dm+Cn> R:
			R=dm+Cn			
		else: 
			return dm+Cn

def SUMTest(itask,HPTasks):
	
	R=0
	Tn=itask['period']
	if itask['sslength']==0:
		R=ssRTA(itask['execution'],HPTasks,Tn)
	else:
		for iseg in itask['Cseg']:
			R+=ssRTA(iseg,HPTasks,Tn)
			if R > Tn:
				return False

	if R+itask['sslength'] > Tn:
		return False
	else:
		return True
def segTest(Cn,Sn,Tn,HPTasks):
	R=0

	while True:	

		dm=0
		for itask in HPTasks:		
			if itask['sslength']==0:
				dm+=itask['execution']*math.ceil((R)/itask['period'])	
			else:
				dm+=MRBF(R,itask)
		
		if dm+Cn+Sn> Tn:
			return False
		 
		if dm+Cn+Sn>R:
			R=dm+Cn+Sn
		else:
			return True
def XRTA(Cn,Sn,Tn,HPTasks):
	R=0
	while True:	
		dm=0
		for itask in HPTasks:			
			dm+=(itask['execution']+itask['sslength'])*math.ceil((R)/itask['period'])	
		if dm+Cn+Sn> Tn:
			return False
		if R != dm+Cn+Sn:
			R=dm+Cn+Sn		
		else: 
			if R> Tn:
				return False
			else:
				return True
def sssDT(Cn,Sn,Tn,HPTasks):

	R=0
	while True:		
		dm=highDemandBurst(R,HPTasks)
		if dm+Cn+Sn> Tn:
			return False
		if R != dm+Cn+Sn:
			R=dm+Cn+Sn			
		else: 
			if R> Tn:
				return False
			else:
				return True


def LLB(n,U):
	if U>n*(2**(1/n)-1):
		return False
	else:
		return True
def EDFB(U):
	if U>1:
		return False
	else:
		return True
def SC_RM(tasks):
	U=0
	for itask in tasks:
		U+=(itask['execution']+itask['sslength'])/itask['period']
	n=len(tasks)
	return LLB(n,U)
def SC_EDF(tasks):
	U=0
	for itask in tasks:
		U+=(itask['execution']+itask['sslength'])/itask['period']
	
	return EDFB(U)
def RM(tasks):
	
	for i in xrange(len(tasks)):
		result=0
		HPTasks=tasks[:i]
		#print HPTasks
		Cn=tasks[i]['execution']
		Sn=tasks[i]['sslength']
		Tn=tasks[i]['period']
		if sssDT(Cn,Sn,Tn,HPTasks)==False:
			return False

	return True
#return T-S
def dm_cmp(x, y):
	dx=x['period']-x['sslength']
	dy=y['period']-y['sslength']
	return int(dx - dy)

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
def BURST_RM(tasks):
	#sorting tasks by increasing period
	sortedTasksRM=sorted(tasks, key=lambda item:item['period']) 
	#print sortedTasksLM
	for i in xrange(len(sortedTasksRM)):
		HPTasks=sortedTasksRM[:i]
		#print HPTasks
		Cn=sortedTasksRM[i]['execution']
		Sn=sortedTasksRM[i]['sslength']
		Tn=sortedTasksRM[i]['period']
		if Burst_HP(Cn,Sn,Tn,sortedTasksRM[:i])==False:
				return False
	return True
def XM(tasks,scheme):
	if scheme == "XLM":
		#sorting tasks by increasing T-S
		sortedTasksLM=sorted(tasks,cmp=dm_cmp)
	elif scheme == "XDM":
		## sort by increasing periods(deadline)
		sortedTasksLM=sorted(tasks, key=lambda item:item['period']) 
	else:
		sys.exit(2)
	#print sortedTasksLM
	for i in xrange(len(sortedTasksLM)):
		HPTasks=sortedTasksLM[:i]
		#print HPTasks
		Cn=sortedTasksLM[i]['execution']
		Sn=sortedTasksLM[i]['sslength']
		Tn=sortedTasksLM[i]['period']
		if XRTA(Cn,Sn,Tn,sortedTasksLM[:i])==False:
				return False
	return True

def LM(tasks,blk=False):
	
	#sorting tasks by increasing T-S
	sortedTasksLM=sorted(tasks,cmp=dm_cmp)
	#print sortedTasksLM
	for i in xrange(len(sortedTasksLM)):
		result=0
		HPTasks=sortedTasksLM[:i]
		#print HPTasks
		Cn=sortedTasksLM[i]['execution']
		Sn=sortedTasksLM[i]['sslength']
		Tn=sortedTasksLM[i]['period']
		if blk == True:
			B= ssBlkTA(sortedTasksLM[i]['sslength'],sortedTasksLM[:i])			
			if B < sortedTasksLM[i]['period']:
				sortedTasksLM[i]['blocking']=B
			else:
				sortedTasksLM[i]['blocking']=sortedTasksLM[i]['period']
			if sssBlkDT(Cn,Sn,Tn,sortedTasksLM[:i])==False:
				return False
		else:
			if sssDT(Cn,Sn,Tn,sortedTasksLM[:i])==False:
				return False

	return True
def NC(tasks):
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

			if sssNCDT(Cn,Sn,Tn,primeTasks) == True:
				
				priortyassigned[i]=1

				canLevel=1
				#print "assign success at",i
				break	
		if canLevel == 0:
			#print "fail assign at",plevel 
			return False 
	return True
def NCSC(tasks):
	#Optimal Priority Assignment
	priortyassigned=[0 for i in range(len(tasks))]
	numnctasks=0
	for plevel in range(len(tasks)): 
		canLevel=0
		
		## check whether task i can be assigned with the priority level plevel
		if numnctasks == 0:
			for i in range(len(tasks)):	
				##ignore lower priority tasks
				if priortyassigned[i]==2:
					continue	
				itask=tasks[i]
				canAssign=1	
				## get higher prioirty tasks
				primeTasks=[]
				for j in range(len(tasks)):
					if (priortyassigned[j]==0 or priortyassigned[j]==1) and i != j:
						primeTasks.append(tasks[j])
					
				
				Tn=itask['period']
				Cn=itask['execution']
				Sn=itask['sslength']
				if sssNCDT(Cn,Sn,Tn,primeTasks) == True:
					priortyassigned[i]=1
					numnctasks+=1
		
		if numnctasks!=0:
			
			for i in range(len(tasks)):	
				##only neccesary condiion
				if priortyassigned[i]!=1:
					continue
				itask=tasks[i]
				
				## get higher prioirty tasks
				primeTasks=[]
				for j in range(len(tasks)):
					if (priortyassigned[j]==0 or priortyassigned[j]==1) and i != j:
						primeTasks.append(tasks[j])	
				Tn=itask['period']
				Cn=itask['execution']
				Sn=itask['sslength']
				if sssDT(itask,primeTasks) == True:					
					priortyassigned[i]=2
					canLevel=1
					numnctasks-=1
					break	
		

		if canLevel == 0:			
			return False 
	return True
def Audsley(tasks,scheme):
	#print tasks
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
			Cn=itask['execution']
			Sn=itask['sslength']
			if scheme == "SUM":
				if SUMTest(itask,primeTasks) == True:
					priortyassigned[i]=1
					canLevel=1
					tasks[i]['priority']=len(tasks)-plevel
					break	
			elif scheme == "FILL":
				if segTest(Cn,Sn,Tn,primeTasks) == True:
					priortyassigned[i]=1
					canLevel=1
					tasks[i]['priority']=len(tasks)-plevel
					break	
			elif scheme == "PASS-OPA":
				if sssDT(Cn,Sn,Tn,primeTasks)==True:
					priortyassigned[i]=1
					canLevel=1
					tasks[i]['priority']=len(tasks)-plevel
					break	
			elif scheme == "SCAIR-OPA":
				if (segTest(Cn,Sn,Tn,primeTasks) or SUMTest(itask,primeTasks) )==True:
					priortyassigned[i]=1
					canLevel=1
					tasks[i]['priority']=len(tasks)-plevel
					break	
			else:
				sys.exit(2)

		if canLevel == 0:
			#print "fail assign at",plevel 
			return False 
	
	return True

def scair_dm(tasks):
	# shortest period first
	sortedTasks = sorted(tasks, key=lambda item: item['period'])

	accept = True
	# test highest-prio task first
	for i in range(len(sortedTasks)):
		Tn = sortedTasks[i]['period']
		Cn = sortedTasks[i]['execution']
		Sn = sortedTasks[i]['sslength']

		# tasks with higher prio than current task
		primeTasks = []
		if i != 0:
			primeTasks = sortedTasks[:i]
			# print('complete: ' + repr(primeTasks))
			# print('part:' + repr(sortedTasks[0:i-1]))

		# if primeTasks:
		if (segTest(Cn, Sn, Tn, primeTasks) or SUMTest(sortedTasks[i], primeTasks)) != True:
			accept = False
	return accept