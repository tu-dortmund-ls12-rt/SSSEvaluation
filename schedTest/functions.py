# Compare-value function for tasks
# Input: Task x
# Output: Difference of Period and Suspension Length of Task x
def lm_cmp(x):
	return x["period"]-x["sslength"]

# Calculate the maximum workload of a higher priority Task with carry-in
# Input: T - Period Length, C - Execution Time, WCRT - Worst-Case-Response-Time, t - Current time
# Output: Total possible Execution Time of Task
def Workload_w_C(T,C,WCRT,t):
	n=int((t-C+WCRT)/T)	
	return n*C+min(C,t-C+WCRT-T*n)

