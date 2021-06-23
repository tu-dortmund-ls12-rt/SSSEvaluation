# FROM https://ieeexplore.ieee.org/document/7809868
# Utilization-Based Method For EDF by Dong and Liu -- RTSS 2016
# Both Schedulability tests give the same results as suspension oblivious (see EMSOFT20 paper by Guenzel, vdBrueggen and Chen).
import math # math.ceil(), math.floor()
import itertools

def UDLEDF(tasks):
	return UDLEDF_improved(tasks)

# Theorem 1 but with suspension oblivious if the test fails
# Input: Task set
# Output: Schedulability test under UDLEDF
def UDLEDF_simple(tasks):
	E = []
	v = []
	Tmax = 0
	totalutil = 0
	for i in range(len(tasks)):
		E.append(tasks[i]['execution'] + tasks[i]['sslength'])
		v.append(tasks[i]['sslength']/tasks[i]['period'])
		if tasks[i]['period'] > Tmax:
			Tmax = tasks[i]['period']
		totalutil += tasks[i]['execution'] / tasks[i]['period']
	E = sorted(E)
	v = sorted(v, reverse = True) # highest first
	# find k
	k = 0
	#check if equation 2 holds
	for k in range(1,len(tasks)):
		sumEi = 0
		for i in range(int(math.floor(k/2.0))):
			sumEi += E[i]
			if sumEi >= Tmax:
				break

	# Suspension-Oblivious if eq. 2 does not hold, or with lower k if it holds
	checkval = 0
	checkval += totalutil
	for i in range(int(k)):
		checkval += v[i]

	return checkval <= 1

# Calculate the sum of suspension ratios of the task set
# Input: Task set
# Output: Schedulability test under UDLEDF
def UDLEDF_ret(tasks):  # returns the checkval without totalutil
	E = []
	v = []
	Tmax = 0
	# totalutil = 0
	for i in range(len(tasks)):
		E.append(tasks[i]['execution'] + tasks[i]['sslength'])
		v.append(tasks[i]['sslength']/tasks[i]['period'])
		if tasks[i]['period'] > Tmax:
			Tmax = tasks[i]['period']
		# totalutil += tasks[i]['execution'] / tasks[i]['period']
	E = sorted(E)
	v = sorted(v, reverse = True) # highest first
	# find k
	k = 0
	#check if equation 2 holds
	for k in range(1,len(tasks)):
		sumEi = 0
		for i in range(int(math.floor(k/2.0))):
			sumEi += E[i]
			if sumEi >= Tmax:
				break

	# test:
	checkval = 0
	# checkval += totalutil
	for i in range(int(k)):
		checkval += v[i]

	return checkval  # <= 1


# Improved utilization-based schedulability test from theorem 2
# Input: Task set
# Output: Schedulability test under UDLEDF
def UDLEDF_improved(tasks):
	#E = []
	v = []
	totalutil = 0
	for i in range(len(tasks)):
		v.append(tasks[i]['sslength']/tasks[i]['period'])
		totalutil += tasks[i]['execution'] / tasks[i]['period']
	
	# test susp obl
	checkval = 0
	checkval += totalutil
	for i in range(len(tasks)):
		checkval += v[i]
	if checkval <=1:
		return True


	# test with subsets of T:
	indicesList = [0] * len(tasks)
	counter = 0
	while counter < pow(2,len(tasks)):
		htasks = [tasks[i] for i in range(len(indicesList)) if indicesList[i] == 1]
		checkval = 0
		# add total utilization
		checkval += totalutil
		# add the suspension ratios from the subset
		checkval += UDLEDF_ret(htasks)
		# add the suspension ratios from the original set - subset
		checkval += sum([v[i] for i in range(len(indicesList)) if indicesList[i] == 0])
		if checkval <=1:
			return True
		counter += 1
		indicesList = nextIndicesList(indicesList)
	return False

# Returns the next combination of the list
# Input: Previous list of indices
# Output: Next step of indices 
def nextIndicesList(indicesList):
    for i in range(0, len(indicesList)):
        if indicesList[i]== 0:
            indicesList[i]=1
            break
        else:
            indicesList[i]=0
    return indicesList