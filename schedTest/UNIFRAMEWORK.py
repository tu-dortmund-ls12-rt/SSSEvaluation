# Schedulability test from "A Unifying Response Time Analysis Framework for
# Dynamic Self-Suspending Tasks" from Chen, Nelissen, Huang in 2016
# https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2016-chen-report-850.pdf
import math


# Compute one entry of the sum on the left hand side from Equation 4.
# Input: Time, total suspension time, vector assignment, worst-case response time, execution time, period
# Output: Total time used by entry task
def compute_sum_entry_Eq4(t, Q, x, R, C, T):
	return C*math.ceil((t+Q+(1-x)*(R-C))/T)


# Compute the left hand side from Equation 4.
# Input: Current task, higher priority tasks, assignment vectors, current time, suspension times
# Output: Total time used by all task
def compute_lhs_Eq4(task, HPTasks, vec_x, t, Q):
	total = task['execution'] + task['sslength']
	# for itask, ix in zip(HPTasks, vec_x):
	for idx in range(len(HPTasks)):
		itask = HPTasks[idx]
		ix = vec_x[idx]
		total += compute_sum_entry_Eq4(
			t, Q[idx], ix, itask['wcrt_uniframework'],
			itask['execution'], itask['period'])
	return total


# Compute vector for linear approximation, using Equation 27
# Input: Tasks, higher priority tasks, assignment vector
# Output: Worst-case response time
def compute_WCRT_bound(task, HPTasks, vec_x):
	# Compute the response time bound using Theorem 1.
	# Given: vector x

	# Compute Q.
	Q = []
	Qvar = 0.0
	for idx in range(len(HPTasks)-1, 0-1, -1):  # from right to left
		Qvar += HPTasks[idx]['sslength']*vec_x[idx]
		Q.insert(0, Qvar)
	# for itask, ix in zip(HPTasks, vec_x):
	# Q += itask['sslength']*ix

	# TDA.
	t = task['execution'] + task['sslength']
	while True:
		wcrt = compute_lhs_Eq4(task, HPTasks, vec_x, t, Q)
		if (wcrt > task['deadline']  # deadline miss
				or wcrt <= t):  # Eq 4 holds
			break
		t = wcrt  # increase t for next iteration

	return wcrt

# Compute vector for linear approximation, using Equation 27
# Input: Tasks, current task index
# Output: Assignment vector
def compute_vec_lin_approx(tasks, index):

	vec_x = []
	sumU = 0
	for idx in range(index):
		itask = tasks[idx]  # task under consideration
		iutil = itask['execution']/itask['period']  # util
		sumU += iutil  # sum of utilizations

		# Compute lhs and rhs of Eq 27.
		lhs = iutil * (itask['wcrt_uniframework'] - itask['execution'])
		rhs = itask['sslength'] * sumU

		# Cases.
		if lhs > rhs:
			vec_x.append(1)
		else:
			vec_x.append(0)
	return vec_x


# Compute vector to dominate Equation 2 (suspension as release jitter). Specified in Lemma 16.
# Input: Tasks, current task index
# Output: Assignment vector
def vec_dominate_eq2(tasks, index):
	vec_x = []
	for _ in range(index):
		vec_x.append(0)
	return vec_x


# Compute vector to dominate Equation 3 (suspension as blocking). Specified in Lemma 17, technical report proof.
# Input: Tasks, current task index
# Output: Assignment vector
def vec_dominate_eq3(tasks, index):
	vec_x = []
	for idx in range(index):
		if tasks[idx]['sslength'] <= tasks[idx]['execution']:
			vec_x.append(1)
		else:
			vec_x.append(0)
	return vec_x


# Schedulability test form the paper using the vector from eq 27 (linear approximation) and the vectors to dominate Eq 2 and Eq 3.
# Input: Tasks ordered by priority
# Output: Schedulability of task set
def UniFramework(tasks):
	for idx in range(len(tasks)):
		vec_lin = compute_vec_lin_approx(tasks, idx)
		vec2 = vec_dominate_eq2(tasks, idx)
		vec3 = vec_dominate_eq3(tasks, idx)

		wcrt_lin = compute_WCRT_bound(tasks[idx], tasks[:idx], vec_lin)
		wcrt2 = compute_WCRT_bound(tasks[idx], tasks[:idx], vec2)
		wcrt3 = compute_WCRT_bound(tasks[idx], tasks[:idx], vec3)

		wcrt = min(wcrt_lin, wcrt2, wcrt3)

		if wcrt > tasks[idx]['deadline']:  # deadline miss
			return False
		else:
			tasks[idx]['wcrt_uniframework'] = wcrt  # set wcrt
			continue
	return True