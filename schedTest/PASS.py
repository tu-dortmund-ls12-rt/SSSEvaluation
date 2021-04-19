from schedTest import WCRT
def PASS(CS,Tn,HPTasks):
	if WCRT.WCRT(CS,Tn,HPTasks)>Tn:
		return False
	else:
		return True
	