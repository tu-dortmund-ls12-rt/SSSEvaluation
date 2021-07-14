# Compare-value function for tasks
# Input: Task x
# Output: Difference of Period and Suspension Length of Task x
def lm_cmp(x):
	return x["period"]-x["sslength"]