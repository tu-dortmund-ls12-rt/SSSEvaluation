# Evaluation Framework for Self-Suspending Task Systems

The provided Python framework evaluates scheduling algorithms and the related schedulability tests based on randomly generated implicit-deadline task sets. The evaluation setup can be configured using multiple parameters like the number of tasks, the utilization range that is considered, the relative length of the suspension interval, the number of sets per configuration, etc..

An overview of the framework can be found in these papers:

[WATERS19](https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/WATERS_2019_paper_8.pdf):
>Georg von der Brüggen, Milad Nayebi, Junjie Shi, Kuan-Hsun Chen, and Jian-Jia Chen, Evaluation Framework for Self-Suspending Task Systems, 10th International Workshop on Analysis Tools and Methodologies for Embedded and Real-time Systems (WATERS 2019), July 2019 

[RTSS21](https://daes.cs.tu-dortmund.de/storages/daes-cs/r/Bilder/Beschaeftigte/M._Sc._Mario_Guenzel/publications/guenzel21rtss_eval.pdf):
>Mario Günzel, Harun Teper, Kuan-Hsun Chen, Georg von der Brüggen, and Jian-Jia Chen, Work-in-Progress: Evaluation Framework for Self-Suspending Schedulability Tests, 42nd IEEE Real-Time Systems Symposium (RTSS 2021), December 2021


Our goal is to provide an easy to use evaluation framework with a pre-implemented task generator, some pre-implemented schedulability tests, and an integrated plotting tool to compare these schedulability tests under the same conditions.

This framework supports the following Self-Suspending Task models:
1. The segmented model, where the self-suspension behaviour is described by a precise pattern of interleaving execution segments and suspension intervals.
2. The dynamic model, where the self-suspension behaviour is described by two upper bounds on the total worst-case execution time (WCET) and the total suspension time. It assumes that a task can suspend itself an infinite amount of times as long as the upper bound on the total suspension time is respected.
3. The hybrid model, that provides different tradeoffs between the overly flexible dynamic model and the overly restrictive segmented model. It assumes different levels of information in addition to the bounds on WCET and suspension time, i.e., the number of suspension segments.

![GUI of the framework](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/images/framework_gui.png)

## Framework Setup and Overview

### Installation

The following steps explain how to deploy this framework on a machine:

First, clone the git repository or download the [zip file](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/archive/refs/heads/master.zip):
```
git clone https://github.com/tu-dortmund-ls12-rt/SSSEvaluation.git
```
Then install the following packages:
```
sudo apt-get install git python3
pip install PyQt5 numpy mip gurobipy matplotlib scipy
```
To activate the full feature set of the framework, you also need to install the Gurobi Optimizer, found at https://www.gurobi.com/. For research purposes you can obtain an academic license, which is used for some of the scheduling algorithms. You can request a license at https://www.gurobi.com/academia/academic-program-and-licenses/. The installation guide can be found at https://www.gurobi.com/documentation/9.1/quickstart_linux/software_installation_guid.html.

Some methods might use the ```timeout``` method. 
Under MacOS, this needs to be installed (e.g., via ```brew install coreutils```).

### How to use?

Move into the end-to-end folder and start the framework with python:
```
cd SSSEvaluation
python3 effsstsMain.py
```

You can now select the parameters for the schedulability analysis.

In the **General** tab you can select whether you want to generate, save or load the task sets for the analysis. If you want to load a task set, you can specify the name of the file, which will be loaded from the **tasksets/saves** folder. Additionally you can select the number of threads for the execution of the analysis and the seed for the task generation.

After that you can select the parameters for the task set in the **Configuration** tab. This includes the number of tasks per set, the number of task sets, the utilization values and the number of computation segments. Moreover, minimal and maximal value for the maximal suspension time can be set, i.e., the maximal suspension time is between the minimum suspension length value and maximum suspension length value multiplied with the difference between the period and execution time.

In the **Schedulability tests** tab you can select any of the schedulability tests which are implemented in the framework. Additionally you can set custom parameters for some of the tests.

After that, the **Plots** tab lets you specify how to plot the schedulability tests. You can plot each test individually, combine all selected tests or combine available tests, if they were previously plotted and their data is available in the **effsstsPlot/Data** folder.

After running the schedulability analysis, you can find the results in the **effsstsPlot/Data** folder.

### How to load and evaluate your own task sets?

You can load individually created task sets into the framework to evaluate them with the implemented schedulability tests.

To load task sets, you need to create a serialized file of your task sets and the parameters that were used to create them. In order to make the process easier, you can use the **SaveTaskSet** script in **tasksets** folder, which will guide you through the process of saving your task sets in a serialized format.

You need to prepare a csv-file containing all task sets for all utilization values you want to evaluate. You can find an example file and the description for it in the **tasksets/input** folder. Copy your csv-file into the **tasksets/input** folder and execute the script. The output file should be in the **tasksets/saves** folder.

After generating your serialized file, you can select the **Load Taskset** option in the **General** tab of the framework and enter the name of the saved task set. After that you can select any number of schedulability tests to run and evaluate.

### How to integrate the framework into your code?

You can integrate the evaluation functionality of this framework into your code. In order to do so, you need to import the **effsstsMain** package which provides three functions to use:

1. evaluate_single_taskset_single_scheme: Takes a single task set as a dictionary and a single scheme and returns the schedulability result.
2. evaluate_single_taskset_multiple_schemes: Takes a single task set as a dictionary and a list of schemes and returns the schedulability result for each scheme.
3. evaluate_multiple_tasksets_multiple_schemes: Takes a list of task sets as dictionaries and a list of schemes and returns the schedulability result for each task set under each schedulability test.

The names for the schedulability tests schemes are identical as the ones in the GUI. For some tests you additionally need to add the parameters at the end of the scheme. For float parameters, please use the decimal point as a separator.

## Implementation Details

To evaluate the schedulability tests, the framework implements a task model, that includes all the information needed for the analysis. Each task is implemented as a dictionary in Python, which includes its period ['period'], execution time ['execution'], utilization ['utilization'], deadline ['deadline'], suspension length ['sslength'], the set of computation segments ['Cseg'] and suspension segments ['Sseg'].

The task creation is done in several steps. First the utilization ['utilization'] is computed, using the UUnifast algorithm. Then the period ['period'] and deadline ['deadline'] are drawn from a log-uniform distribution with two orders of magnitude, which are used to compute the execution time. The suspension time ['sslength'] is drawn uniformly from the interval between the minimum suspension length value and maximum suspension length value, which are specified in the GUI, multiplied with the difference between period and execution time.

After that, the hybrid model is generated. For each task, multiple paths are generated, which consist of alternating computation and suspension segments, starting with a computation segment. For each path, the UUniFast algorithm is used to segment the total computation and total suspension time. This results in the sum of the computation and suspension segments being equal to the total execution and segmentation time of each task.

Then the segmented model is generated, which creates a worst-case path regarding each segment individually. The computation and suspension times of each segment are upper bounds of the corresponding segments of each path. The segments are saved in the task's ['Cseg'] and ['Sseg'] keys.

For the dynamic model, the total execution time ['execution'] and total suspension time ['sslength'] of each task are updated in the final step. For each path, the total computation and suspension time is computed and the maximum value of each is saved.

## Schedulability Tests

### Not limited

Name | Paper | File name | Method name
---|---|---|---
SCEDF | https://link.springer.com/article/10.1007/s11241-018-9316-9 Section 7.1 | SCEDF.py | SC_EDF
SCRM | https://link.springer.com/article/10.1007/s11241-018-9316-9 Section 4.2.4 | SCRM.py | SC_RM
SUSPOBL | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspObl

### Segmented Suspension

#### Implicit-Deadline

Name | Paper | File name | Method name
---|---|---|---
EDA | https://ieeexplore.ieee.org/document/7010483 | EDA.py | SEIFDA
SEIFDA-minD | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-maxD | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-PBminD | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-MILP | https://dl.acm.org/doi/10.1145/2997465.2997497 | mipx.py | mip
NC | https://dl.acm.org/doi/10.1145/2997465.2997497 | NC.py | NC
PROPORTIONAL | https://ieeexplore.ieee.org/document/6881366 | PROPORTIONAL.py | PROPORTIONAL
SRSR | https://dl.acm.org/doi/abs/10.1145/2997465.2997485 | SRSR.py | SRSR
UPPAAL | https://ieeexplore.ieee.org/document/8715111 <sup>1</sup>| Uppaal.py | UPPAAL

[1]: (The implementation can only be used under Linux currently due to limitations of the ```schedTest/verifyta``` file. We noticed that UPPAAL runs very slow in our framework which looks like non-responsive behavior. Try reduing the timeout within ```UPPAAL.py``` and using the non-GUI version in ```effsstsMain.py```.)

#### Constrained-Deadline

Name | Paper | File name | Method name
---|---|---|---
EDAGMF-OPA | https://ieeexplore.ieee.org/document/7459469 | pass_opa.py | PASS_OPA
MILP-ReleaseJitter| https://ieeexplore.ieee.org/document/7176028 | milp_response.py | Milpreleasejitter 
SCAIR-RM | https://www.semanticscholar.org/paper/Schedulability-and-Priority-Assignment-for-Tasks-Huang-Chen/d2b0871a6826957d75b1473690ec8eaa6ea05d86 | rad.py | scair_dm
SCAIR-OPA | https://www.semanticscholar.org/paper/Schedulability-and-Priority-Assignment-for-Tasks-Huang-Chen/d2b0871a6826957d75b1473690ec8eaa6ea05d86 | pass_opa.py | PASS_OPA
Casini18 | https://ieeexplore.ieee.org/abstract/document/8603232 | casini18.py | Casini18

#### Arbitrary-Deadline

Name | Paper | File name | Method name
---|---|---|---
GMFPA | https://link.springer.com/article/10.1007/s11241-017-9279-2 | GMFPA.py | GMFPA

### Dynamic Suspension

#### Implicit-Deadline

Name | Paper | File name | Method name
---|---|---|---
Idv-Burst-RM | https://ieeexplore.ieee.org/document/7010485 | Burst_RM.py | BURST_RM 
RSS | https://ieeexplore.ieee.org/document/9211430 Section V | RSS.py | RSS
UDLEDF | http://zheng.eng.wayne.edu/_resources/pdfs/HRT.pdf <sup>2</sup> | UDLEDF.py | UDLEDF
WLAEDF | https://www.cs.unc.edu/~anderson/papers/ecrts13e_erratum.pdf <sup>2</sup>  | WLAEDF.py | WLAEDF
RTEDF  | https://ieeexplore.ieee.org/document/9211430 Algorithm 1 | RTEDF.py | RTEDF
SUSPBLOCK | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspBlock

[2]: (Uniprocessor version presented in https://ieeexplore.ieee.org/document/9211430 Section III)

#### Constrained-Deadline

Name | Paper | File name | Method name
---|---|---|---
PASS-OPA | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7167340 | pass_opa.py | PASS_OPA
UNIFRAMEWORK | https://ieeexplore.ieee.org/abstract/document/7557869 Section V | UNIFRAMEWORK.py | UniFramework
SUSPJIT | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspJit

#### Arbitrary-Deadline

Name | Paper | File name | Method name
---|---|---|---

### Hybrid Suspension

#### Implicit-Deadline

Name | Paper | File name | Method name
---|---|---|---
Oblivious-IUB- | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Clairvoyant-SSSD- | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Oblivious-MP- | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Clairvoyant-PDAB- | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath

#### Constrained-Deadline

Name | Paper | File name | Method name
---|---|---|---

#### Arbitrary-Deadline

Name | Paper | File name | Method name
---|---|---|---


## File Structure
    .
    ├── effsstsPlot	
    │   ├── Data			    # Includes all output graphs
    │   └── effsstsPlot.py	    # Output graph generation
    ├── images                  # Framework icons and images	
    ├── schedTest			    # Contains all schedulability tests
    │   ├── inputs			    # Temporary Inputs for schedulability tests
    │   └── temp_models		    # Temporary models for schedulability tests
    ├── tasksets			    # Contains all schedulability tests
    │   ├── input			    # Contains the input files for the SaveTaskSet.py script
    │   ├── saves			    # Contains the output files of the SaveTaskSet.py script, aswell as all saved task sets that can be loaded into the framework.
    │   ├── CreateCsvFile.py	# Script to create a .csv file from a task set dictionary.
    │   └── SaveTaskSet.py      # Script to create a task set dictionary from a .csv file.
    ├── effsstsMain.py		    # Framework executable
    ├── gurobi.env			    # Settings for Gurobi optimizer
    └── README.md
    
## How to integrate your algorithms?

You can extend the framework with other scheduling algorithms written in Python or C++.
* To integrate your algorithms, you need to include your Python implementation in the **schedTest** folder. Alternatively for C++-algorithms, you need a pre-built binary, which can be executed from a Python script. 
* Then you need to extend the framework interface, so that you can select your schedulability test in the GUI. In order to do so, you need to add several things in the effsstsMain.py file:
    1.  Import your Python file.
    2.  Add an entry to the GUI, which you can later select. 
    3.  Each selected test adds a scheme to a list, which includes all tests that will be executed. In case your schedulability test gets selected, you need to add your scheme, so that the algorithm is later called.
    4.  Add an additional case to the switchTest method, which will select and execute your schedulability test, if you added your scheme correctly.
* In order to make the implementation easier, you can search for an existing implementation, for example 'RSS' and copy each step to implement your own algorithm. 

## ToDo
The following algorithms are not implemented yet:
* Sporadic version of UPPAAL: The test integrated in the framework is the PERIODIC version. A SPORADIC version exists and could also be added to the framework
* Sus-Aware FP with arbitrary deadlines and arrival curves: https://ieeexplore.ieee.org/abstract/document/9622374
* EDF-Like Analysis: https://ieeexplore.ieee.org/abstract/document/9984793

Possible advancements in the future:
* Include tasks with release jitter
* Use DRS for task generation
* Multicore

## Acknowledgements

We would like to thank all the authors who helped to extend the framework. In particular, we would like to thank Bo Peng, Morteza Mohaqeqi, Alessandro Biondi and Beyazit Yalcinkaya for providing the source code and additonal information of their work.

This work has been supported by Deutsche Forschungsgemeinschaft (DFG), as part of Sus-Aware (Project No. 398602212), and by the Deutsche Forschungsgemeinschaft (DFG, German Research Foundation) – Projektnummer 124020371 – SFB 876.
