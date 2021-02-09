def dbfNC1(task,t):
	return int((t+task['sslength'])/task['period'])*task['Cseg'][1]+int((t-(task['period']-task['sslength']))/task['period'])*task['Cseg'][0]
def dbfNC2(task,t):
	return int((t+(task['sslength']))/task['period'])*task['Cseg'][0]+int((t)/task['period'])*task['Cseg'][1]
def dbfNC(t,task):
	return max(dbfNC1(task,t),dbfNC2(task,t))
def NC(tasks):
	
	for i in range(len(tasks)):
		task=tasks[i]
		D=(task['period']-task['sslength'])

		dbf=0
		
		for jtask in tasks:
			dbf+=dbfNC(D,jtask)
		if dbf>D:
			return False

		D=(task['period'])
		
		dbf=0
		HEPTasks=tasks[:i+1]
		for jtask in tasks:
			dbf+=dbfNC(D,jtask)
		if dbf>D:
			return False
	return True