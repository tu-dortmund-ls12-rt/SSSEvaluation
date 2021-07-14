from __future__ import division
import math
import sys

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
def FRDGMF(task,HPTasks,D):
	# For each execution segment, calculate the interfering workload from higher priority tasks
	mi = len(task['Cseg'])
	for j in range(mi):
		# Current time point t
		t = 0
		# Workload at time point t
		wl = task['Cseg'][j]
		while t <= D and wl > t:
			# Set t to current workload time
			t = wl
			# Set workload to c_i^j + interfering workload from higher priority tasks
			wl = 0
			for hptask in HPTasks:
				wl += workload(hptask,mi,t,D)
			wl += task['Cseg'][j]
		# Not schedulable if workload greater than time or time greater than deadline
		if wl > t or t > D:
			return False
	# Every computation segment schedulable
	return True

def workload(hptask,mi,t,D):

	c_segs = hptask['Cseg']
	s_segs = hptask['Sseg']
	s_segs.append(hptask['period']-hptask['deadline'])
	t_segs = [D+s_segs[i] for i in range(mi)]

	# Determine maximum interference from higher priority tasks
	max_sum_h = 0

	# Test each segment as starting point
	for h in range(mi):

		# Determine upper bound l of execution-segments of hptask
		t_sum = 0
		# Determine sum of periods of hptask
		l = 0
		while t >= t_sum:
			t_sum += t_segs[(h+l)%mi]
			if t >= t_sum:
				l += 1
		
		t_sum -= t_segs[(h+l)%mi]
		
		#Calculate sum of execution segments
		l_temp = l
		c_sum = 0
		while l_temp > 0:
			c_sum += c_segs[(h+l_temp-1)%mi]
			l_temp -= 1

		# Determine minimum interference from execution segment or remaining time
		c_min = min(c_segs[(h+l)%mi], t-t_sum)

		# Interference as sum of execution segments
		eih = c_sum + c_min

		# Replace maximum interference if necessary
		if eih > max_sum_h:
			max_sum_h = eih
			
	# Return maximum interference of higher priority task
	return max_sum_h

def PASS(CS,Tn,HPTasks):
	if WCRT(CS,Tn,HPTasks)>Tn:
		return False
	else:
		return True

def WCRT(CS,Tn,HPTasks):	
	R=0
	while True:
		if R> Tn:
			return R
		I=0
		for itask in HPTasks:
			I=I+Workload_w_C(itask['period'],itask['execution'],itask['period'],R)
		if I+CS>R:
			R=I+CS
		else:
			return R

# Calculate the maximum workload of a higher priority Task with carry-in
# Input: T - Period Length, C - Execution Time, WCRT - Worst-Case-Response-Time, t - Current time
# Output: Total possible Execution Time of Task
def Workload_w_C(T,C,WCRT,t):
	n=int((t-C+WCRT)/T)	
	return n*C+min(C,t-C+WCRT-T*n)


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
