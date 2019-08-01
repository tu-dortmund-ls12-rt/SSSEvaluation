#include <ctime>
#include <cstdlib>
#include <iostream>
#include <fstream>
#include <vector>
#include <iterator>

#include "generator.h"
#include "rta_ss.h"
#include "delay_bound.h"
#include "parser.h"

using namespace std;


void test_ui_rt(){
    std::string t_schedulable;
    try{
        SS_taskset_t SStaskset = parserUI();

        SS_Task_RTA analysis0(SStaskset);
        if (analysis0.isSchedulable()) {
            t_schedulable = "True";
        } else {
            t_schedulable = "False";
        }
    }
    catch(exception &e){
        cout << e.what() << endl;
    }

    std::remove("py_input.txt");
    const char *path="rt_result.txt";
    std::ofstream file(path); //open in constructor
    std::string data(t_schedulable);
    file << data;
}

int main(int argc, char* argv[]) {
    srand(0);

    test_ui_rt();
    return 0;
}

