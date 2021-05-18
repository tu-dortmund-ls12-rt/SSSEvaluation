from schedTest import functions

def dbfEDA(t,task,ssofftypes):
	sum=0
	for i in range(ssofftypes):
		sum+=task['Cseg'][i]

	D=(task['period']-task['sslength'])/ssofftypes
	if t<D:
		return 0
	else:
		return sum+(t-D)*(sum)/task['period']

def EDA(tasks, ssofftypes):
	sortedTasks=sorted(tasks,key= lambda x: functions.lm_cmp(x))
	for i in range(len(sortedTasks)):
		task=sortedTasks[i]
		D=(task['period']-task['sslength'])/ssofftypes
		dbf=0
		HEPTasks=sortedTasks[:i+1]
		for jtask in HEPTasks:
			dbf+=dbfEDA(D,jtask,ssofftypes)
		if dbf>D:
			return False
	return True
