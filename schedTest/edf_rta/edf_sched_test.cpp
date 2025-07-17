//
//  edf_sched_test.cpp
//  edf_response_time_xcode
//
//  Created by Zakaria Al-Jumaei on 12.07.25.
//

#include "models.h"
#include "dss_rta.h"
#include <vector>
#include <random>
#include <iostream>
#include <future>
#include <fstream>
#include <sstream>
#include <string>

using namespace std;

std::random_device rd;
std::mt19937 rng(rd());


/*
 ------------------------------------------------
 task in this project through the class DssTask:
 DssTask::DssTask(int wcet, int suspension, int period, int deadline, int wcrt_ub)
 {
     this->wcet = wcet;
     this->suspension = suspension;
     this->period = period;
     this->deadline = deadline;
     this->wcrt_ub = wcrt_ub;
 }
 -------------------------------------------------
 Framework >>>   This Project(rta)
 execution       wcet
 sslenght        suspension
 period          period
 deadline        deadline
                 wcrt_ub=0
 --------------------------------------------------
 the format of created csv file in the Framework:
 create csv file in this fromat:
     wcet | suspension | period | deadline
     value| value      | value   | value
     value| value      | value   | value
     ....
 
 Command : g++ models.cpp rta.cpp  dss_rta.cpp edf_sched_test.cpp  -o edf_sched_test
          ./edf_sched_test tasks.csv
 */
vector<DssTask> read_tasks_from_csv_file(const string& fileName){
    //cout << "read from csv file:" << endl;
    
    vector<DssTask> tasks;
    
    ifstream file(fileName);
    
    if(!file.is_open()){
        runtime_error("Faild to open file:" + fileName);
    }
    string line;
    // 1) Skip header >> wcet | suspension | period | deadline
    getline(file, line);
    //cout << "first line is readed and skipped " << endl;

    int i = 0;
    // 2) pars another lines
    while (getline(file, line)) {
        //cout << "While-loop:  " << i++ << endl;
        
        istringstream ss(line);
        string field;
        int wcet, susp, period, deadline;

        // wcet
        getline(ss, field, ',');
        wcet = stoi(field);
        
        // suspension
        getline(ss, field, ',');
        susp = stoi(field);
        // period
        getline(ss, field, ',');
        period = stoi(field);
        // deadline
        getline(ss, field, ',');
        deadline = stoi(field);

        tasks.emplace_back(wcet, susp, period, deadline, /*wcrt_ub=*/0);
        
    }
    return tasks;
    
        
    
}

int main(int args, char* argv[]){
    if(args != 2){
        cout << "provide two arguments" << endl;
    }
    string fileName = argv[1];
    
    vector<DssTask> tasks;
    
    try {
        tasks = read_tasks_from_csv_file(fileName);
    } catch (const exception& e) {
        cerr << "Error reading CSV: " << e.what() << "\n";
        return 2;
    }
    //cout << "All tasks after parseing from Json:" << endl;
    
    /*for(auto task : tasks){
        cout <<"wcet: " << task.get_wcet() << endl;
        cout <<"suspension: " << task.get_suspension() << endl;
        cout <<"period: " << task.get_period() << endl;
        cout <<"deadline: " << task.get_deadline() << endl;
    }*/
    bool sched = dss_rta::analyze_task_set(tasks, true);

    if (sched == false) {
        cout << "false" << endl;
    }else{
        cout << "true" << endl;
    }
    
    return 1;
}

DssTask generate_task(double utilization, int min_period, int max_period, double min_susp_factor, double max_susp_factor, double deadline_factor)
{
    DssTask task;

    task.set_wcrt_ub(0);

    return task;
}
