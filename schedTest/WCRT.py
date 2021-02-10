import math
from schedTest import functions

# From: https://ieeexplore.ieee.org/abstract/document/9211430 Section IV.
# Calculation of the Worst-Case-Response-Time (WCRT) for a given task and a set of higher priority tasks
# Input: CS - ExecutionTime, Tn - Task Period Length, HPTasks - Higher Priority Task Set
# Output: R - WCRT

def WCRT(CS,Tn,HPTasks):	
	R=0
	while True:
		if R> Tn:
			return R
		I=0
		for itask in HPTasks:
			I=I+functions.Workload_w_C(itask['period'],itask['execution'],itask['period'],R)
		if I+CS>R:
			R=I+CS
		else:
			return R