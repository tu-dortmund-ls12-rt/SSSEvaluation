// dss_rta.h
// Implements the proposed analysis approach for self-suspending tasks under EDF scheduling

#pragma once
#include "models.h"
#include <vector>

namespace dss_rta {
	// Analyze a task set of self-suspending tasks
	bool analyze_task_set(std::vector<DssTask>& task_set, bool return_on_schedulable);

	// Runs unit tests for this module
	bool test();
}
