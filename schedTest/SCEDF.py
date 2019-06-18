def EDFB(U):
	if U>1:
		return False
	else:
		return True
def SC_EDF(tasks):
	U=0
	for itask in tasks:
		U+=(itask['execution']+itask['sslength'])/itask['period']
	
	return EDFB(U)