def LLB(n,U):
	if U>n*(2**(1/n)-1):
		return False
	else:
		return True
def SC_RM(tasks):
	U=0
	for itask in tasks:
		U+=(itask['execution']+itask['sslength'])/itask['period']
	n=len(tasks)
	return LLB(n,U)