// models.cpp
// Defines model classes for sporadic tasks with jitter and self-suspending tasks

#include "models.h"

// SeqTask class
SeqTask::SeqTask()
{
	wcet = 0;
	jitter = 0;
	period = 0;
	deadline = 0;
	wcrt_ub = 0;
}

SeqTask::SeqTask(int wcet, int jitter, int period, int deadline, int wcrt_ub)
{
	this->wcet = wcet;
	this->jitter = jitter;
	this->period = period;
	this->deadline = deadline;
	this->wcrt_ub = wcrt_ub;
}

void SeqTask::set_wcet(int wcet)
{
	this->wcet = wcet;
}

int SeqTask::get_wcet() const
{
	return wcet;
}

void SeqTask::set_period(int period)
{
	this->period = period;
}

int SeqTask::get_period() const
{
	return period;
}

void SeqTask::set_deadline(int deadline)
{
	this->deadline = deadline;
}

int SeqTask::get_deadline() const
{
	return deadline;
}

void SeqTask::set_jitter(int jitter)
{
	this->jitter = jitter;
}

int SeqTask::get_jitter() const
{
	return jitter;
}

void SeqTask::set_wcrt_ub(int wcrt_ub)
{
	this->wcrt_ub = wcrt_ub;
}

int SeqTask::get_wcrt_ub() const
{
	return wcrt_ub;
}

double SeqTask::get_utilization() const
{
	return static_cast<double>(wcet) / static_cast<double>(period);
}

std::ostream& operator<<(std::ostream& os, SeqTask const& seq_task)
{
	os << "C=" << seq_task.wcet << "\tJ=" << seq_task.jitter << "\tT=" << seq_task.period << "\tD=" << seq_task.deadline << "\tR=" << seq_task.wcrt_ub;
	return os;
}

// DssTask class
DssTask::DssTask()
{
	wcet = 0;
	suspension = 0;
	period = 0;
	deadline = 0;
	wcrt_ub = 0;
}

DssTask::DssTask(int wcet, int suspension, int period, int deadline, int wcrt_ub)
{
	this->wcet = wcet;
	this->suspension = suspension;
	this->period = period;
	this->deadline = deadline;
	this->wcrt_ub = wcrt_ub;
}

void DssTask::set_wcet(int wcet)
{
	this->wcet = wcet;
}

int DssTask::get_wcet() const
{
	return wcet;
}

void DssTask::set_period(int period)
{
	this->period = period;
}

int DssTask::get_period() const
{
	return period;
}

void DssTask::set_deadline(int deadline)
{
	this->deadline = deadline;
}

int DssTask::get_deadline() const
{
	return deadline;
}

void DssTask::set_suspension(int suspension)
{
	this->suspension = suspension;
}

int DssTask::get_suspension() const
{
	return suspension;
}

void DssTask::set_wcrt_ub(int wcrt_ub)
{
	this->wcrt_ub = wcrt_ub;
}

int DssTask::get_wcrt_ub() const
{
	return wcrt_ub;
}

double DssTask::get_utilization() const
{
	return static_cast<double>(wcet) / static_cast<double>(period);
}

std::ostream& operator<<(std::ostream& os, DssTask const& dss_task)
{
	os << "C=" << dss_task.wcet << "\tS=" << dss_task.suspension << "\tT=" << dss_task.period << "\tD=" << dss_task.deadline << "\tR=" << dss_task.wcrt_ub;
	return os;
}

// Performs unit tests for this module
bool models::test()
{
	SeqTask seq_task(100, 100, 100, 100, 100);
	seq_task.set_wcet(10);
	seq_task.set_jitter(20);
	seq_task.set_period(30);
	seq_task.set_deadline(40);
	seq_task.set_wcrt_ub(50);
	if (seq_task.get_wcet() != 10) {
		return false;
	}
	if (seq_task.get_jitter() != 20) {
		return false;
	}
	if (seq_task.get_period() != 30) {
		return false;
	}
	if (seq_task.get_deadline() != 40) {
		return false;
	}
	if (seq_task.get_wcrt_ub() != 50) {
		return false;
	}

	seq_task = SeqTask(10, 20, 30, 40, 50);
	if (seq_task.get_wcet() != 10) {
		return false;
	}
	if (seq_task.get_jitter() != 20) {
		return false;
	}
	if (seq_task.get_period() != 30) {
		return false;
	}
	if (seq_task.get_deadline() != 40) {
		return false;
	}
	if (seq_task.get_wcrt_ub() != 50) {
		return false;
	}

	DssTask dss_task(100, 100, 100, 100, 100);
	dss_task.set_wcet(10);
	dss_task.set_suspension(20);
	dss_task.set_period(30);
	dss_task.set_deadline(40);
	dss_task.set_wcrt_ub(50);
	if (dss_task.get_wcet() != 10) {
		return false;
	}
	if (dss_task.get_suspension() != 20) {
		return false;
	}
	if (dss_task.get_period() != 30) {
		return false;
	}
	if (dss_task.get_deadline() != 40) {
		return false;
	}
	if (dss_task.get_wcrt_ub() != 50) {
		return false;
	}

	dss_task = DssTask(10, 20, 30, 40, 50);
	if (dss_task.get_wcet() != 10) {
		return false;
	}
	if (dss_task.get_suspension() != 20) {
		return false;
	}
	if (dss_task.get_period() != 30) {
		return false;
	}
	if (dss_task.get_deadline() != 40) {
		return false;
	}
	if (dss_task.get_wcrt_ub() != 50) {
		return false;
	}

	return true;
}
