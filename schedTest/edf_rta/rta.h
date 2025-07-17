// rta.h
// Implements the WCRT analysis for sporadic tasks with jitter by Spuri ("Analysis of deadline scheduled real-time systems", Research report, 1996)

#pragma once
#include "models.h"
#include <vector>

namespace rta {
	// Check necessary conditions for the schedulability of a task set of sporadic tasks with jitter
	bool check_necessary_condition(const std::vector<SeqTask> task_set);

	// Get the WCRT of a task in the task set (efficient version: safely skips redundant values of the offset variable)
	int get_wcrt(const std::vector<SeqTask> seq_tasks, const int task_index);

	// Get the WCRT of a task in the task set (inefficient version: evaluates all possible values of the offset variable)
	int get_wcrt_inefficient(const std::vector<SeqTask> seq_tasks, const int task_index);

	// Get the WCRT of each task in the task set and evaluate the schedulability of the task set
	bool analyze_task_set(std::vector<SeqTask>& seq_tasks);
	
	// Runs unit tests for this module
	bool test();
}
