# FROM https://ieeexplore.ieee.org/abstract/document/9211430 Section III
# Workload-Based Method For EDF by Liu and Anderson -- ECRTS 2013
import math # math.ceil(), math.floor()

# Calculate the workload for non-carry-in jobs
# Input: Current tasks 'i','j', upper-bound 'xil', suspension tick 'slj', task set 'tasks'
# Output: Workload for non-carry-in jobs
def Wnc(i, l, xil, slj, tasks):
	val=0
	if i != l:
		val = min(math.floor(xil/tasks[i]['period'])*tasks[i]['execution'], xil - tasks[l]['execution'] - slj + 1)
	else:
		val = min(math.floor(xil/tasks[l]['period'])*tasks[l]['execution'] - tasks[l]['execution'], xil - tasks[l]['period'])
	return val

# Calculate the workload for carry-in jobs
# Input: Current tasks 'i','j', upper-bound 'xil', suspension tick 'slj', task set 'tasks'
# Output: Workload for carry-in jobs
def Wc(i, l, xil, slj, tasks):
	val=0
	if i != l:
		val = min( Delta(i, xil, tasks), xil - tasks[l]['execution'] - slj + 1 )
	else:
		val = min( Delta(l, xil, tasks) - tasks[l]['execution'], xil - tasks[l]['period'] )
	return val

# Calculate the minimum workload for the carry-in job
# Input: Current tasks 'i', upper-bound 't', task set 'tasks'
# Output: Mimimum workload in the interval [i,t] with carry-in job
def Delta(i, t, tasks):
	val = 0
	val += ( math.ceil(t/tasks[i]['period']) -1 ) * tasks[i]['execution']
	val += min( tasks[i]['execution'], t - math.ceil(t/tasks[i]['period']) * tasks[i]['period'] + tasks[i]['period'] )
	return val

# Workload-based schedulability test from theorem 2
# Input: Task set
# Output: Schedulability test under WLAEDF
def WLAEDF(tasks):
	#calculate the total execution time and the total utilization
	sumexec = 0
	totalutil = 0
	for i in range(len(tasks)):
		sumexec += tasks[i]['execution']
		totalutil += tasks[i]['execution']/tasks[i]['period']
	#for each task
	for l in range(len(tasks)):
		#for each suspension tick
		for slj in range(int(tasks[l]['sslength'])+1):
			#calculate the upper bound of the time interval
			upperbound = math.ceil((tasks[l]['execution'] + slj + sumexec)/(1.0-totalutil))
			#for each timestep between the period length and the upper bound, calculate the total workload up until that point
			for xil in range(int(tasks[l]['period']), int(upperbound)):
				checkval = 0
				#calculate the workload for all suspending and non-suspending tasks
				for i in range(len(tasks)):
					if tasks[i]['sslength'] != 0:
						checkval += max(Wnc(i, l, xil, slj, tasks), Wc(i, l, xil, slj, tasks))
					else:
						checkval += Wnc(i, l, xil, slj, tasks)
				#only schedulable if the test holds every time
				if checkval > xil - tasks[l]['execution'] - slj:
					return False
	return True