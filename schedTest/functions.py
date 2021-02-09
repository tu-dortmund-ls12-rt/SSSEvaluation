def lm_cmp(x):
	return x["period"]-x["sslength"]

def Workload_w_C(T,C,WCRT,t):
	n=int((t-C+WCRT)/T)	
	return n*C+min(C,t-C+WCRT-T*n)

