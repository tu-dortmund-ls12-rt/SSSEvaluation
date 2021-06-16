from __future__ import division
from schedTest import functions
import random
import math
import json
import sys, getopt
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
		print('test.py -i <seed> -u <totalutilzation> -if <scalefactor>')
		sys.exit(2)
	print(opts, args)
	
	for opt, arg in opts:
		if opt == '-h':
			print('test.py -s <randoseed> -u <totalutilzation> -f <scalefactor>')
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
		#print("tjump:",tjump,"l:",l)
		for j in range(i,l+1):			
			D+=itask["Cseg"][j%numcseg]			

		if D > maxD:
			maxD=D
	#print("t: ",t,"d:",maxD,itask)
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


def dbfEDA(t,task):
	D=(task['period']-task['sslength'])/2
	if t<D:
		return 0
	else:
		return task['Cseg'][0]+task['Cseg'][1]+(t-D)*(task['Cseg'][0]+task['Cseg'][1])/task['period']

def dbf1(task,t,d):
	return int((t+task['period']-d)/task['period'])*task['Cseg'][0]+int(t/task['period'])*task['Cseg'][1]
def dbf2(task,t,d):
	return int((t+d+task['sslength'])/task['period'])*task['Cseg'][1]+int((t+task['sslength'])/task['period'])*task['Cseg'][0]
def dbf1FPTAS(task,t,d,k):

	if t>=(k-1)*task['period']+d:
		return t*(task['Cseg'][0]+task['Cseg'][1])/task['period']-d*task['Cseg'][0]/task['period']+task['Cseg'][0]
	else:
		return dbf1(task,t,d)
def dbf2FPTAS(task,t,d,k):

	if t>=(k-1)*task['period']+task['period']-task['sslength']-d:
		return (t+task['sslength'])*(task['Cseg'][0]+task['Cseg'][1])/task['period']+d*task['Cseg'][1]/task['period']
	else:
		return dbf2(task,t,d)

def SEIFDA(task,HindexTasks,k,scheme):
	if scheme=='minD':
		if task['Cseg'][0]<task['Cseg'][1]:
			d1=task['Cseg'][0]
		else:
			d1=(task['period']-task['sslength'])-task['Cseg'][1]
	elif scheme=='maxD':
		d1=(task['period']-task['sslength'])/2
	elif scheme=='PBminD':
		if task['Cseg'][0]+task['Cseg'][1] ==0:
			print("0")
			d1=0
		else:
			if task['Cseg'][0]<task['Cseg'][1]:
				d1=(task['period']-task['sslength'])*task['Cseg'][0]/(task['Cseg'][0]+task['Cseg'][1])
			else:
				d1=task['period']-task['sslength']-(task['period']-task['sslength'])*task['Cseg'][1]/(task['Cseg'][0]+task['Cseg'][1])
	
	while 1:

		if task['Cseg'][0]<task['Cseg'][1]:
			d=d1
			c=task['Cseg'][0]
		else:
			d=(task['period']-task['sslength'])-d1
			c=task['Cseg'][1]
		if d>(task['period']-task['sslength'])/2 or d<c:
			return d1
		t=[]
		for a in range(1,k+1):
			for itask in HindexTasks:
				t.append(itask['d1']+(a-1)*itask['period'])
				t.append((a-1)*itask['period'])
				t.append(itask['period']-(itask['d1']+itask['sslength'])+(a-1)*itask['period'])
				t.append(itask['period']-itask['sslength']+(a-1)*itask['period'])

			t.append(d1+(a-1)*task['period'])
			t.append((a-1)*task['period'])
			t.append(task['period']-(d1+task['sslength'])+(a-1)*task['period'])
			t.append(task['period']-task['sslength']+(a-1)*task['period'])
		flag=False
		#print(len(t))
		for it in t:
			dbf=0
			for itask in HindexTasks:
				d=itask['d1']
				dbf+=max(dbf1FPTAS(itask,it,d,k),dbf2FPTAS(itask,it,d,k))
			dbf+=max(dbf1FPTAS(task,it,d1,k),dbf2FPTAS(task,it,d1,k))
			if dbf >it:
				flag=True
				break
		#print(d1)
		if flag==True:
			if scheme=='minD' or scheme=='PBminD':
				if task['Cseg'][0]<task['Cseg'][1]:
					d1=d1+1
				else:
					d1=d1-1
			else:
				if task['Cseg'][0]<task['Cseg'][1]:
					d1=d1-1
				else:
					d1=d1+1

			continue
		else:
			return d1
			
def greedy(tasks,scheme):
	sortedTasks=sorted(tasks,key= lambda x: functions.lm_cmp(x))
	
	ischme=scheme.split('-')[1]
	k=int(scheme.split('-')[2])
	#print(k)

	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		HindexTasks=sortedTasks[:i]
		
		d1=SEIFDA(task,HindexTasks,k,ischme)
		if task['Cseg'][0]>=task['Cseg'][1]:
			d=(task['period']-task['sslength'])-d1
			c=task['Cseg'][1]
		else:
			d=d1
			c=task['Cseg'][0]
		if d>(task['period']-task['sslength'])/2 or d<c:

			return False
		else:
			task['d1']=d1

		
		
	# 	D=(task['period']-task['sslength'])/2
	# 	dbf=0
	# 	HEPTasks=sortedTasks[:i+1]
	# 	for jtask in HEPTasks:
	# 		dbf+=dbfEDA(D,jtask)
	# 	if dbf>D:
	# 		return False
	t=[]
	for a in range(1,k+1):
		for itask in tasks:
			t.append(itask['d1']+(a-1)*itask['period'])
			t.append((a-1)*itask['period'])
			t.append(itask['period']-(itask['d1']+itask['sslength'])+(a-1)*itask['period'])
			t.append(itask['period']-itask['sslength']+(a-1)*itask['period'])

	
	#print(len(t))
	for it in t:
		dbf=0
		for itask in tasks:
			d=itask['d1']
			dbf+=max(dbf1FPTAS(itask,it,d,k),dbf2FPTAS(itask,it,d,k))
		if dbf>it:
			print(dbf,d,'false')
		
	return True
def EDA(tasks):
	sortedTasks=sorted(tasks,key= lambda x: functions.lm_cmp(x))
	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		D=(task['period']-task['sslength'])/2
		dbf=0
		HEPTasks=sortedTasks[:i+1]
		for jtask in HEPTasks:
			dbf+=dbfEDA(D,jtask)
		if dbf>D:
			return False
	return True
def RM(tasks):
	
	for i in range(len(tasks)):
		result=0
		HPTasks=tasks[:i]
		#print(HPTasks)
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
	#print(sortedTasksLM)
	for i in range(len(sortedTasksRM)):
		HPTasks=sortedTasksRM[:i]
		#print(HPTasks)
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
	#print(sortedTasksLM)
	for i in range(len(sortedTasksLM)):
		HPTasks=sortedTasksLM[:i]
		#print(HPTasks)
		Cn=sortedTasksLM[i]['execution']
		Sn=sortedTasksLM[i]['sslength']
		Tn=sortedTasksLM[i]['period']
		if XRTA(Cn,Sn,Tn,sortedTasksLM[:i])==False:
				return False
	return True

def LM(tasks,blk=False):
	
	#sorting tasks by increasing T-S
	sortedTasksLM=sorted(tasks,cmp=dm_cmp)
	#print(sortedTasksLM)
	for i in range(len(sortedTasksLM)):
		result=0
		HPTasks=sortedTasksLM[:i]
		#print(HPTasks)
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

	