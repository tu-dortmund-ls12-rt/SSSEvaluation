# FROM https://ieeexplore.ieee.org/document/7809868
# Utilization-Based Method For EDF by Dong and Liu -- RTSS 2016
# Both Schedulability tests give the same results as suspension oblivious (see EMSOFT20 paper by Guenzel, vdBrueggen and Chen).
import math # math.ceil(), math.floor()
import itertools


def UDLEDF(tasks):
	return UDLEDF_improved(tasks)

# Lemma 4 but with suspension oblivious if the test fails
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


# Improved utilization-based schedulability test from lemma 6
# Input: Task set
# Output: Schedulability test under UDLEDF
def UDLEDF_improved(tasks): 
	E = []
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
	indiceslist = getsubindices(len(tasks))
	for ind in indiceslist:
		htasks = []
		checkval = 0
		# add total utilization
		checkval += totalutil
		# add the suspension ratios from the subset
		for i in ind:
			htasks.append(tasks[i])
		checkval += UDLEDF_ret(htasks)
		# add the suspension ratios from the original set - subset
		for i in range(len(tasks)):
			if i not in ind:
				checkval += v[i]
		if checkval <=1:
			return True
	return False


# Returns all possible sets of an array of length n
# Input: Array Length
# Output: Array of subarray-indices
def getsubindices(n):
	indices = []
	for i in range(n):
		indices.append(i)
	indiceslist = []
	for i in range(1,n+1):
		indiceslist.extend(list(itertools.combinations(indices, i)))
	return indiceslist
