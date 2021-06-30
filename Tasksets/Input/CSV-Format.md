Format of a valid csv-file to load task sets:

You need to specify all tasks for all task sets for each utilization step. Each line represents one task of that specific task set and utilization value. First you need to specify all task sets for each utilization value in ascending order in regard to the utilization value. Then you need to specify all tasks for each task set, which should be ordered by period.

Each line has the following information about one task:

Period - Execution - Deadline - Utilization - SuspensionLenght - minimumSuspensionRatio - Paths - Cseg - Sseg

Example: Two task sets with two tasks per set and utilization interval [0.1-0.15] with an utilization step of 0.05

Each line represents the task of that task set and utilization value.

Line | Utilization | Task set | Task
|---|---|---|---|
1|Utilization 0.10 | Taskset 1.1 | Task 1.1.1
2|Utilization 0.10 | Taskset 1.1 | Task 1.1.2
3|Utilization 0.10 | Taskset 1.2 | Task 1.2.1
4|Utilization 0.10 | Taskset 1.2 | Task 1.2.2
5|Utilization 0.15 | Taskset 2.1 | Task 2.1.1
6|Utilization 0.15 | Taskset 2.1 | Task 2.1.2
7|Utilization 0.15 | Taskset 2.2 | Task 2.2.1
8|Utilization 0.15 | Taskset 2.2 | Task 2.2.2
