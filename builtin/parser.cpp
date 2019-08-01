#include "delay_bound.h"

#include <cstdlib>
#include <cmath>
#include <algorithm>
#include <iostream>
#include <fstream>


#define EPS 0.0001



SS_taskset_t parserUI()
{
	
  //the output of taskset
    SS_taskset_t taskset;
    std::string file_path("rtss2016/py_input.txt");
    std::ifstream in_s(file_path);

    if(in_s)
    {
        std::string line, value, tok;

        std::vector <std::string> vec;
        while(getline(in_s, line))
        {
            SS_task_t task;
            std::stringstream  linestream(line);
            while(getline(linestream,value,','))
                vec.push_back(value);

            int num_c = std::stoi( vec[0]);
            int num_s = std::stoi(vec[4+num_c]);
	    task.T = std::stod(vec[3+num_c]);
	    task.D = std::stod(vec[5+num_c+num_s]);
	    for(int i = 1; i<= num_c; i++)
		task.C.push_back(std::stod(vec[i]));
	    for(int i = 1; i<= num_s; i++)
		task.S.push_back(std::stod(vec[4+num_c+i]));

             //push it into the task vector (taskset)
            taskset.push_back(task);
            vec.clear();
        }

        in_s.close();
    }
    else
        std::cout << "Could not open: " + file_path << std::endl;
  return taskset;
}



