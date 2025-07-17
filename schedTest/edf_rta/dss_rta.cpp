// dss_rta.cpp
// Implements the proposed analysis approach for self-suspending tasks under EDF scheduling

#include "dss_rta.h"
#include "rta.h"

// Check necessary conditions for the schedulability of a task set of self-suspending tasks
bool check_necessary_conditions(const std::vector<DssTask> task_set)
{
	double system_utilization = 0.0;
	for (const auto& task : task_set) {
		if (task.get_deadline() > task.get_period()) {
			return false;
		}
		if ((task.get_wcet() + task.get_suspension()) > task.get_deadline()) {
			return false;
		}
		system_utilization += task.get_utilization();
		if (system_utilization > 1.0) {
			return false;
		}
	}

	return true;
}

// Get task set of sporadic tasks with jitter for the analysis of a given task in the task set
std::vector<SeqTask> get_seq_task_set(const std::vector<DssTask> task_set, const int task_index, const std::vector<int> wcrt_bounds)
{
	std::vector<SeqTask> seq_task_set(task_set.size());
	
	for (auto j = 0; j < task_set.size(); j++) {
		seq_task_set[j].set_deadline(task_set[j].get_deadline());
		seq_task_set[j].set_period(task_set[j].get_period());
		if (j == task_index) {
			seq_task_set[j].set_wcet(task_set[j].get_wcet() + task_set[j].get_suspension());
			seq_task_set[j].set_jitter(0);
		}
		else {
			seq_task_set[j].set_wcet(task_set[j].get_wcet());
			seq_task_set[j].set_jitter(wcrt_bounds[j] - task_set[j].get_wcet());
		}
	}

	return seq_task_set;
}

// Analyze a task set of self-suspending tasks
bool dss_rta::analyze_task_set(std::vector<DssTask>& task_set, bool return_on_schedulable)
{
	if (!check_necessary_conditions(task_set)) {
		return false;
	}

	// set initial conditions
	std::vector<int> wcrt_bounds(task_set.size());
	for (auto i = 0; i < task_set.size(); i++) {
		wcrt_bounds[i] = task_set[i].get_deadline();
	}

	// check necessary conditions for transformed task sets
	for (auto i = 0; i < task_set.size(); i++) {
		std::vector<SeqTask> seq_task_set = get_seq_task_set(task_set, i, wcrt_bounds);
		if (!rta::check_necessary_condition(seq_task_set)) {
			return false;
		}
	}

	// iteratively refine wcrt bounds
	bool update = true;
	bool all_schedulable = true;
	while (update) {
		update = false;
		std::vector<int> wcrts(task_set.size());

		// get wcrts from jitter rta
		for (auto i = 0; i < task_set.size(); i++) {
			std::vector<SeqTask> seq_task_set = get_seq_task_set(task_set, i, wcrt_bounds);

			int wcrt = rta::get_wcrt(seq_task_set, i);

			if (wcrt > -1) {
				wcrts[i] = wcrt; // keep previous result in case of overflow of busy length calculation
			}

			if (wcrts[i] < wcrt_bounds[i]) {
				wcrt_bounds[i] = wcrts[i];
				update = true;
			}
		}
		
		// check schedulability
		all_schedulable = true;
		for (auto i = 0; i < task_set.size(); i++) {
			if (wcrts[i] > task_set[i].get_deadline()) {
				all_schedulable = false;
			}
		}
		if (all_schedulable) {
			for (auto i = 0; i < task_set.size(); i++) {
				task_set[i].set_wcrt_ub(wcrt_bounds[i]);
			}
			if (return_on_schedulable) {
				return true;
			}
		}
	}

	return all_schedulable;
}

// Runs unit tests for this module
bool dss_rta::test()
{
	// test necessary conditions
	std::vector<DssTask> task_set(3);
	task_set[0] = DssTask(1, 0, 3, 3, 0);
	task_set[1] = DssTask(1, 0, 3, 3, 0);
	task_set[2] = DssTask(2, 0, 3, 3, 0);
	if (check_necessary_conditions(task_set)) {
		return false;
	}
	task_set[2] = DssTask(0, 0, 3, 5, 0);
	if (check_necessary_conditions(task_set)) {
		return false;
	}
	task_set[2] = DssTask(0, 1, 5, 3, 0);
	if (!check_necessary_conditions(task_set)) {
		return false;
	}
	task_set[2] = DssTask(1, 1, 5, 2, 0);
	if (!check_necessary_conditions(task_set)) {
		return false;
	}
	task_set[2] = DssTask(1, 4, 5, 2, 0);
	if (check_necessary_conditions(task_set)) {
		return false;
	}

	// test transformation
	task_set = std::vector<DssTask>(2);
	task_set[0] = DssTask(1, 2, 4, 4, 0);
	task_set[1] = DssTask(2, 0, 6, 6, 0);
	std::vector<int> wcrt_bounds(task_set.size());
	wcrt_bounds[0] = 4;
	wcrt_bounds[1] = 6;
	std::vector<SeqTask> seq_task_set = get_seq_task_set(task_set, 0, wcrt_bounds);
	if (seq_task_set[0].get_wcet() != 3) {
		return false;
	}
	if (seq_task_set[0].get_jitter() != 0) {
		return false;
	}
	if (seq_task_set[0].get_deadline() != task_set[0].get_deadline()) {
		return false;
	}
	if (seq_task_set[0].get_period() != task_set[0].get_period()) {
		return false;
	}
	if (seq_task_set[1].get_wcet() != 2) {
		return false;
	}
	if (seq_task_set[1].get_jitter() != 4) {
		return false;
	}
	if (seq_task_set[1].get_deadline() != task_set[1].get_deadline()) {
		return false;
	}
	if (seq_task_set[1].get_period() != task_set[1].get_period()) {
		return false;
	}
	seq_task_set = get_seq_task_set(task_set, 1, wcrt_bounds);
	if (seq_task_set[0].get_wcet() != 1) {
		return false;
	}
	if (seq_task_set[0].get_jitter() != 3) {
		return false;
	}
	if (seq_task_set[0].get_deadline() != task_set[0].get_deadline()) {
		return false;
	}
	if (seq_task_set[0].get_period() != task_set[0].get_period()) {
		return false;
	}
	if (seq_task_set[1].get_wcet() != 2) {
		return false;
	}
	if (seq_task_set[1].get_jitter() != 0) {
		return false;
	}
	if (seq_task_set[1].get_deadline() != task_set[1].get_deadline()) {
		return false;
	}
	if (seq_task_set[1].get_period() != task_set[1].get_period()) {
		return false;
	}

	// violation of necessary conditions for transformed tasks
	task_set[0] = DssTask(1, 2, 4, 4, 0);
	task_set[1] = DssTask(2, 0, 6, 6, 0);
	if (analyze_task_set(task_set, true)) {
		return false;
	}

	// schedulable with first wcrt bounds
	task_set[0] = DssTask(1, 2, 8, 8, 0);
	task_set[1] = DssTask(2, 0, 6, 6, 0);
	if (!analyze_task_set(task_set, true)) {
		return false;
	}
	if (task_set[0].get_wcrt_ub() != 7) {
		return false;
	}
	if (task_set[1].get_wcrt_ub() != 3) {
		return false;
	}

	// schedulable with refined wcrt bounds
	if (!analyze_task_set(task_set, false)) {
		return false;
	}
	if (task_set[0].get_wcrt_ub() != 5) {
		return false;
	}
	if (task_set[1].get_wcrt_ub() != 3) {
		return false;
	}

	// fail due to deadline violation
	task_set[0] = DssTask(1, 1, 4, 3, 0);
	task_set[1] = DssTask(2, 1, 6, 6, 0);
	if (analyze_task_set(task_set, true)) {
		return false;
	}

	return true;
}
