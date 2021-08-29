# Typical fixed priority analyses using TDA.
# E.g. specified in "A Unifying Response Time Analysis Framework for
# Dynamic Self-Suspending Tasks" from Chen, Nelissen, Huang in 2016
# https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2016-chen-report-850.pdf
import math

# Suspension oblivious test, given by Eq 1.
# Input: Task set
# Output: Schedulability of task set
def SuspObl(tasks):
	for idx in range(len(tasks)):
		wcrt = SuspObl_WCRT(tasks[idx], tasks[:idx])
		if wcrt > tasks[idx]['deadline']:  # deadline miss
			return False
		else:
			tasks[idx]['wcrt_obl'] = wcrt  # set wcrt
			continue
	return True

# Compute the response time bound using Eq 1.
# Input: Task, higher priority tasks
# Output: Worst-case response time of task
def SuspObl_WCRT(task, HPTasks):
	t = task['execution'] + task['sslength']
	while True:
		# Compute lhs of Eq 1.
		wcrt = task['execution'] + task['sslength']
		for itask in HPTasks:
			wcrt += math.ceil(t/itask['period'])*(
				itask['execution']+itask['sslength'])
		if (wcrt > task['deadline']  # deadline miss
				or wcrt <= t):  # Eq 1 holds
			break
		t = wcrt  # increase t for next iteration
	return wcrt

# Suspension as release jitter, given by Eq 2.
# Input: Task set
# Output: Schedulability of task set
def SuspJit(tasks):
	for idx in range(len(tasks)):
		wcrt = SuspJit_WCRT(tasks[idx], tasks[:idx])
		if wcrt > tasks[idx]['deadline']:  # deadline miss
			return False
		else:
			tasks[idx]['wcrt_jit'] = wcrt  # set wcrt
			continue
	return True

# Compute the response time bound using Eq 2.
# Input: Task, higher priority tasks
# Output: Worst-case response time of task
def SuspJit_WCRT(task, HPTasks):
	t = task['execution'] + task['sslength']
	while True:
		# Compute lhs of Eq 2.
		wcrt = task['execution'] + task['sslength']
		for itask in HPTasks:
			wcrt += math.ceil(
				(t + itask['wcrt_jit'] - itask['execution'])/itask['period']
				)*itask['execution']
		if (wcrt > task['deadline']  # deadline miss
				or wcrt <= t):  # Eq 2 holds
			break
		t = wcrt  # increase t for next iteration
	return wcrt

# Suspension as blocking, given by Eq 3.
# Input: Task set
# Output: Schedulability of task set
def SuspBlock(tasks):
	for idx in range(len(tasks)):
		wcrt = SuspBlock_WCRT(tasks[idx], tasks[:idx])
		if wcrt > tasks[idx]['deadline']:  # deadline miss
			return False
		else:
			tasks[idx]['wcrt_block'] = wcrt  # set wcrt
			continue
	return True

# Compute the response time bound using Eq 3.
# Input: Task, higher priority tasks
# Output: Worst-case response time of task
def SuspBlock_WCRT(task, HPTasks):
	# Compute B.
	B = task['sslength']
	for itask in HPTasks:
		B += min(itask['execution'], itask['sslength'])

	t = task['execution'] + task['sslength']
	while True:
		# Compute lhs of Eq 3.
		wcrt = task['execution'] + B
		for itask in HPTasks:
			wcrt += math.ceil(t/itask['period'])*itask['execution']
		if (wcrt > task['deadline']  # deadline miss
				or wcrt <= t):  # Eq 2 holds
			break
		t = wcrt  # increase t for next iteration
	return wcrt