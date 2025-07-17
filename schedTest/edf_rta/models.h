// models.h
// Defines model classes for sporadic tasks with jitter and self-suspending tasks

#pragma once
#include <vector>
#include <iostream>

class SeqTask {
private:
	int wcet; // worst-case execution time
	int deadline; // relative deadline
	int period; // minimum inter-arrival time
	int jitter; // release jitter
	int wcrt_ub; // upper bound on the worst-case response time

public:
	SeqTask();

	SeqTask(int wcet, int jitter, int period, int deadline, int wcrt_ub);

	void set_wcet(int wcet);

	int get_wcet() const;

	void set_period(int period);

	int get_period() const;

	void set_deadline(int deadline);

	int get_deadline() const;

	void set_jitter(int jitter);

	int get_jitter() const;

	void set_wcrt_ub(int wcrt_ub);

	int get_wcrt_ub() const;

	double get_utilization() const;

	friend std::ostream& operator<<(std::ostream& os, SeqTask const& seq_task);
};

class DssTask {
private:
	int wcet; // worst-case execution time
	int deadline; // relative deadline
	int period; // minimum inter-arrival time
	int suspension; // maximum cumulative suspension time
	int wcrt_ub; // upper bound on the worst-case response time

public:
	DssTask();

	DssTask(int wcet, int suspension, int period, int deadline, int wcrt_ub);

	void set_wcet(int wcet);

	int get_wcet() const;

	void set_period(int period);

	int get_period() const;

	void set_deadline(int deadline);

	int get_deadline() const;

	void set_suspension(int suspension);

	int get_suspension() const;

	void set_wcrt_ub(int wcrt_ub);

	int get_wcrt_ub() const;

	double get_utilization() const;

	friend std::ostream& operator<<(std::ostream& os, DssTask const& dss_task);
};

namespace models {
	// Performs unit tests for this module
	bool test();
}
