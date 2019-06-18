import math
from functions import *

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

