from schedTest import rad

def SCAIR_RM(tasks):
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
		if (rad.segTest(Cn, Sn, Tn, primeTasks) or rad.SUMTest(sortedTasks[i], primeTasks)) != True:
			accept = False
	return accept
