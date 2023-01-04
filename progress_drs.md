PLEASE REPORT THE PROGRESS HERE.

The project so far:

- Initially we designed an algorithm to generate tasksets using the DRS(Dirichlet Rescaling) method.

The DRS method: (more info on this link: https://pypi.org/project/drs/#:~:text=The%20Dirichlet%2DRescale%20(DRS),to%20its%20corresponding%20upper%20bound )

- The test gernerating function (taskGeneration_drs) takes 3 parameters (total execution time, total execution time + suspension time and the number of tasks requiured per set) from the user for generating the task set.

- The algorithm then generates a taskset with (period, execution, utilization, suspension length, deadline, Cseg and Sseg. A sample taskset is shown below:

	[{'period': 435.2408514188942, 'execution': 9.33987633671953, 'utilization': 0.02145909858018001, 'sslength': 32.180472206320594, 'deadline': 435.2408514188942, 'Cseg': [1.9037080582515293, 7.436168278468002], 'Sseg': [32.180472206320594], 'paths':}]

- We then tested these tasksets for various Dynamic Algorithms like RSS, WLAEDF, RTEDF and also for various Segmented Scheduling Algorithms like SCEDF, SCRM, SCAIR-RM to name a few.

- For the DRS system we also created a spereate GUI from the UUniFast System. The GUI is able to generate tasksets and also able to test it against the Segmented and Dynamic Algorithms 

- Unlike UUniFast for DRS we introduced 'Granularity' which produces a set number of points in x and y coordinate in the Acceptance ratio vs Execution graph. 

- We created a seperate GUI to perform the DRS tasks as the existing GUI could only perform UUniFast tasks but due to the change in input variables we had to create a seperate GUI to carry out DRS tasks. The DRS GUI takes 'Granularity' instead of 'segment' and 'utilization step' in UUniFast. Also, the DRS GUI is incapble to run the FRD Segmented and FRD Hybrid algorithms yet.


Problems we faced and are :

- During our work we found that the DRS method cannot work and throws an error if the total execution time is set to 0. To fix this issue in the (DRS_ex) fuction we added an exception and then the method could return 0 if and when the total execution is set to 0



Things that needs to be worked upon :


- Although the DRS GUI shows tab for FRD Segmented and FRD Hybrid algorithms but the DRS system is still not able to test those algorithms


