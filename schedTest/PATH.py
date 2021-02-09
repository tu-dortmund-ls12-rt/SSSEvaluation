from __future__ import division
import math
from schedTest import functions

def dbfpath1(task,t,k):
	
	maxG=0

	tg=t-int(t/task['period'])*task['period']
	for p in range(len(task['paths'])):
		if tg<task['paths'][p]['deadline'][0]:
			continue
		else:
			if task['paths'][p]['Cseg'][0]>maxG:
				maxG=task['paths'][p]['Cseg'][0]
	maxd=0		

	if t>=k*task['period']:
		return (t/task['period'])*task['execution']+maxG
	else:
		return int(t/task['period'])*task['execution']+maxG
def dbfpath2(task,t,k,p):
	d2=task['period']-task['paths'][p]['Sseg'][0]-task['paths'][p]['deadline'][0]

	if t<d2:
		return 0
	else:
		return task['paths'][p]['Cseg'][1]+dbfpath1(task,t-d2,k)
def dbfpath(task,t,k):
	
	maxdbf2=0
	for p in range(len(task['paths'])):		
		maxdbf2=max(maxdbf2,dbfpath2(task,t,k,p))
		

	return max(maxdbf2,dbfpath1(task,t,k))
def setDeadline(task,scheme,d,ifsame):
	
	if ifsame == True:
		if scheme == 'minD':

			C1max=0
			C2max=0

			for p in task['paths']:
				C1max=max(C1max,p['Cseg'][0])
				C2max=max(C2max,p['Cseg'][1])
			for p in task['paths']:
				if C1max<C2max:
					p['deadline'][0]=d
					p['deadline'][1]=task['period']-d-p['Sseg'][0]
				else:
					p['deadline'][0]=task['period']-d-p['Sseg'][0]
					p['deadline'][1]=d

		elif scheme == 'PBminD':

			C1max=0
			C2max=0
			for p in task['paths']:
				C1max=max(C1max,p['Cseg'][0])
				C2max=max(C2max,p['Cseg'][1])
			for p in task['paths']:
				if C1max<C2max:
					p['deadline'][0]=d+(task['period']-p['Sseg'][0])*C1max/(C1max+C2max)
					p['deadline'][1]=task['period']-p['deadline'][0]-p['Sseg'][0]
				else:
					p['deadline'][1]=d+(task['period']-p['Sseg'][0])*C2max/(C1max+C2max)
					p['deadline'][0]=task['period']-p['deadline'][1]-p['Sseg'][0]
		else:

			sys.exit()
		return True
	else:
		if scheme=='minD':
			for p in task['paths']:
				if p['Cseg'][0]<p['Cseg'][1]:
					p['deadline'][0]=d
					p['deadline'][1]=task['period']-d-p['Sseg'][0]
				else:
					p['deadline'][0]=task['period']-d-p['Sseg'][0]
					p['deadline'][1]=d
		elif scheme=='PBminD':
			for p in task['paths']:
				if p['Cseg'][0]<=p['Cseg'][1]:
					p['deadline'][0]=d+(task['period']-p['Sseg'][0])*p['Cseg'][0]/(p['Cseg'][0]+p['Cseg'][1])
					p['deadline'][1]=task['period']-p['deadline'][0]-p['Sseg'][0]
				else:
					p['deadline'][1]=d+(task['period']-p['Sseg'][0])*p['Cseg'][1]/(p['Cseg'][0]+p['Cseg'][1])
					p['deadline'][0]=task['period']-p['deadline'][1]-p['Sseg'][0]
		elif scheme=='maxD':
			if task['Cseg'][0]>task['Cseg'][1]:
				for p in task['paths']:
					p['deadline'][0]=d
					p['deadline'][1]=task['period']-d-p['Sseg'][0]
			else:
				for p in task['paths']:
					p['deadline'][0]=task['period']-d-p['Sseg'][0]
					p['deadline'][1]=d
		
		else:			
			sys.exit()

		return True
def TerminationCheck(task,scheme,d1,ifsame):
	if scheme== 'minD' or scheme == 'maxD':		
		if d1>(task['period']-task['sslength'])/2:		
			return True
	elif scheme=='PBminD':
		for p in task['paths']:
			if p['Cseg'][0]<=p['Cseg'][1]:
				ddd=d1+(task['period']-p['Sseg'][0])*p['Cseg'][0]/(p['Cseg'][0]+p['Cseg'][1])
			else:
				ddd=d1+(task['period']-p['Sseg'][0])*p['Cseg'][1]/(p['Cseg'][0]+p['Cseg'][1])
				
			if ddd>(task['period']-p['Sseg'][0])/2:	
				return True
def SEIFDApath(task,HindexTasks,k,scheme,ifsame):

	d1=0
	while 1:			
		
		setDeadline(task,scheme,d1,ifsame)	

		t=[]
		for a in range(1,k+1):
			for itask in HindexTasks+[task]:
				t.append((a-1)*itask['period'])
				for p in range(len(itask['paths'])):
					t.append(itask['paths'][p]['deadline'][0]+(a-1)*itask['period'])			
					t.append(itask['period']-(itask['paths'][p]['deadline'][1]+itask['paths'][p]['Sseg'][0])+(a-1)*itask['period'])
					t.append(itask['period']-itask['paths'][p]['Sseg'][0]+(a-1)*itask['period'])
			
		flag=False
		#print(len(t))
		for it in t:
			dbf=0
			for itask in HindexTasks+[task]:			
				dbf+=dbfpath(itask,it,k)			
			if dbf >it:
				flag=True
				break
		#print(d1)
		if flag==True:
			if scheme=='minD' or scheme=='PBminD':				
				d1=d1+1			
			else:				
				d1=d1-1
		else:
			return True	

		if TerminationCheck(task,scheme,d1,ifsame):
			return False
		
def PATH(tasks,scheme):
	sortedTasks=sorted(tasks,key= lambda x: functions.lm_cmp(x))

	ischme=scheme.split('-')[1]
	k=int(scheme.split('-')[2])
	ifsame=scheme.split('-')[3]=='D=D'
	
	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		HindexTasks=sortedTasks[:i]
		
		if SEIFDApath(task,HindexTasks,k,ischme,ifsame)==False:
			return False		
	t=[]
	for a in range(1,k+1):
		for itask in HindexTasks+[task]:
			t.append((a-1)*itask['period'])
			for p in range(len(itask['paths'])):
				t.append(itask['paths'][p]['deadline'][0]+(a-1)*itask['period'])			
				t.append(itask['period']-(itask['paths'][p]['deadline'][1]+itask['paths'][p]['Sseg'][0])+(a-1)*itask['period'])
				t.append(itask['period']-itask['paths'][p]['Sseg'][0]+(a-1)*itask['period'])
			
	for it in t:
		dbf=0
		for itask in tasks:
			dbf+=dbfpath(itask,it,1000)	
			if dbf>it:
				print(dbf,'false')
				sys.exit()
	return True		