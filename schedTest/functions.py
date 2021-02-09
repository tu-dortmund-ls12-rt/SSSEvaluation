def lm_cmp(x, y):
	#dx=(x["period"]-x["sslength"])/2
	#dy=(y["period"]-y["sslength"])/2
	#return int(dx - dy)
	return 1

def Workload_w_C(T,C,WCRT,t):
	n=int((t-C+WCRT)/T)	
	return n*C+min(C,t-C+WCRT-T*n)

