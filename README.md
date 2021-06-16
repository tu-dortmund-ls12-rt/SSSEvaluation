# Evaluation Framework for Self-Suspending Task Systems

The provided Python framework evaluates scheduling algorithms and the related schedulability tests based on randomly generated implicit-deadline task sets. The evaluation setup can be configured using multiple parameters like the number of tasks, the utilization range that is considered, the relative length of the suspension interval, the number of sets per configuration, etc..

An overview of the framework can be found in this [paper](https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/WATERS_2019_paper_8.pdf):
>Georg von der Brüggen, Milad Nayebi, Junjie Shi, Kuan-Hsun Chen, and Jian-Jia Chen, Evaluation Framework for Self-Suspending Task Systems, 10th International Workshop on Analysis Tools and Methodologies for Embedded and Real-time Systems (WATERS 2019), July 2019 

Our goal is to provide an easy to use evaluation framework with a pre-implemented task generator, some pre-implemented schedulability tests, and an integrated plotting tool to compare these schedulability tests under the same conditions.

This framework support the Self-Suspending Task models:
1. The segmented model, where the self-suspension behaviour is described by a precise pattern of interleaving execution segments and suspension intervals.
2. The dynamic model, where the self-suspension behaviour is described by two upper bounds on the total worst-case execution time (WCET) and the total suspension time. It assumes that a task can suspend itself an infinity amount of times as long as the upper bound on the total suspension time is respected.
3. The hybrid models, that provide different tradeoffs between the overly flexible dynamic model and the overly restrictive segmented model, assuming different levels of information in addition to the bounds on WCET and suspension time, i.e., at least the number of suspensions.#

![GUI of the framework](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/images/framework_gui.jpg)

## Framework Setup and Overview

### Installation

The following steps explain how to deploy this framework on the machine:

First, clone the git repository or download the [zip file](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/archive/refs/heads/master.zip):
```
git clone https://github.com/tu-dortmund-ls12-rt/SSSEvaluation.git
```
Then install the following software:
```
sudo apt-get install git python3
pip install PyQt5 numpy mip gurobipy matplotlib scipy
```
To activate the full feature set of the framework, you also need to install the Gurobi Optimizer, found at https://www.gurobi.com/. For research purposes you can obtain an academic license, which is used for some of the scheduling algorithms. You can request a license at https://www.gurobi.com/academia/academic-program-and-licenses/. The installation guide can be found at https://www.gurobi.com/documentation/9.1/quickstart_linux/software_installation_guid.html.

### How to use?

Move into the end-to-end folder and start the framework with python:
```
cd SSSEvaluation
python3 effsstsMain.py
```

You can now select the parameters for the schedulability analysis.

In the **General** tab you can select the path of your task sets, and if you want to generate, save or load the task sets for the analysis. Additionally you can select the number of threads for the execution of the analysis and the seed for the task generation.

After that you can select the parameters for the task set in the **Configuration** tab. This includes the number of tasks per set, the number of task sets, the utilization values and the number of computation segments. Moreover, minimal and maximal value for the maximal suspension time can be set, i.e., the maximal suspension time is between the minimum suspension length value and maximum suspension length value multiplied with the difference between the period and execution time.

In the **Schedulability tests** tab you can select any of the schedulability tests which are implemented in the framework. Additionally you can set custom parameters for some of the tests.

After that, the **Plots** tab lets you specify how to plot the schedulability tests. You can plot each test individually, combine all selected tests or combine available tests, if they were previously plotted and their data is available in the **effsstsPlot/Data/\*** folder.

After running the schedulability analysis, you can find the results in the **effsstsPlot/Data** folder.

## Implementation Details

To evaluate the schedulability tests, the framework implements a task model, that includes all the information needed for the analysis. Each task is implemented as a dictionary in Python, which includes its period ['period'], execution time ['execution'], utilization ['utilization'], deadline ['deadline'], suspension length ['sslength'], the set of computation segments ['Cseg'] and suspension segments ['Sseg'].

The task creation is done in several steps. First the utilization ['utilization'] is computed, using the UUnifast algorithm. Then the period ['period'] and deadline ['deadline'] are drawn from a log-uniform distribution with two orders of magnitude, which are used to compute the execution time. The suspension time ['sslength'] is drawn uniformly from the interval between the minimum suspension length value and maximum suspension length value, which are specified in the GUI, multiplied with the difference between period and execution time.

After that, the hybrid model is generated. For each task, multiple paths are generated, which consist of alternating computation and suspension segments, starting with a computation segment. For each path, the UUniFast algorithm is used to segment the total computation and total suspension time. This results in the sum of the computation and suspension segments being equal to the total execution and segmentation time of each task.

Then the segmented model is generated, which creates a worst-case path regarding each segment individually. The computation and suspension times of each segment are upper bounds of the corresponding segments of each path. The segments are saved in the tasks ['Cseg'] and ['Sseg'] keys.

For the dynamic model, the total execution time ['execution'] and total suspension time ['sslength'] of each task are updated in the final step. For each path, the total computation and suspension time is computed and the maximum value of each is saved.

## Schedulability Tests

### Segmented Suspension

#### Implicit-Deadline

Name | Paper | File name | Method name
---|---|---|---
SEIFDA-minD- | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-maxD- | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-PBminD- | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-MILP | https://dl.acm.org/doi/10.1145/2997465.2997497 | mipx.py | mip
PROPORTIONAL | https://ieeexplore.ieee.org/document/6881366 | PROPORTIONAL.py | PROPORTIONAL
NC | https://dl.acm.org/doi/10.1145/2997465.2997497 | NC.py | NC
SRSR | https://dl.acm.org/doi/abs/10.1145/2997465.2997485 | SRSR.py | SRSR

#### Constrained-Deadline

Name | Paper | File name | Method name
---|---|---|---
Biondi RTSS 16 | https://ieeexplore.ieee.org/document/7176028 | Biondi.py | Biondi

#### Arbitrary-Deadline

Name | Paper | File name | Method name
---|---|---|---
GMF-PA | https://link.springer.com/article/10.1007/s11241-017-9279-2 | GMFPA.py | GMFPA

### Dynamic Suspension

#### Implicit-Deadline

Name | Paper | File name | Method name
---|---|---|---
EDA | https://ieeexplore.ieee.org/document/7010483 | EDA.py | SEIFDA
RSS | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Section V | RSS.py | SC2EDF
UDLEDF | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Section III | UDLEDF.py | UDLEDF_improved
WLAEDF | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Section III | WLAEDF.py | WLAEDF
RTEDF  | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Algorithm 1 | RTEDF.py | RTEDF

#### Constrained-Deadline

Name | Paper | File name | Method name
---|---|---|---
SCEDF | https://link.springer.com/content/pdf/10.1007/s11241-018-9316-9.pdf Section 7.1 | SCEDF.py | SC_EDF
SCRM | https://link.springer.com/content/pdf/10.1007/s11241-018-9316-9.pdf Section 4.2.4 | SCRM.py | SC_RM
SCAIR-RM | https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2015-technical-report-multi-seg-Kevin.pdf | rad.py | scair_dm
SCAIR-OPA | https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2015-technical-report-multi-seg-Kevin.pdf | rad.py | Audsley
PASS-OPA | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7167340 | Audsley.py | Audsley
Uniframework | https://ieeexplore.ieee.org/abstract/document/7557869 Section V | UNIFRAMEWORK.py | UniFramework
SuspObl | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspObl
SuspJit | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspJit
SuspBlock | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspBlock

#### Arbitrary-Deadline

Name | Paper | File name | Method name
---|---|---|---

### Hybrid Suspension

#### Implicit-Deadline

Name | Paper | File name | Method name
---|---|---|---
Oblivious-IUB | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Clairvoyant-SSSD | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Oblivious-MP | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Clairvoyant-PDAB | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath

#### Constrained-Deadline

Name | Paper | File name | Method name
---|---|---|---

#### Arbitrary-Deadline

Name | Paper | File name | Method name
---|---|---|---


## File Structure
    .
    ├── effsstsPlot	
    │   ├── Data			# Includes all output graphs
    │   └── effsstsPlot.py	# Output graph generation
    ├── images              # Framework icons and images	
    ├── schedTest			# Contains all schedulability tests
    │   ├── inputs			# Temporary Inputs for schedulability tests
    │   └── temp_models		# Temporary models for schedulability tests
    ├── effsstsMain.py		# Framework executable
    ├── gurobi.env			# Settings for Gurobi optimizer
    └── README.md
    
## How to integrate your algorithms?

You can extend the framework with other scheduling algorithms written in Python or C++.
* To integrate your algorithms, you need to include your Python implementation in the schedTest folder. Alternatively for C++-algorithms, you need a pre-built binary, which can be executed from a Python script. 
* Then you need to extend the framework interface, so that you can select your schedulability test in the GUI. In order to do so, you need to add several things in the effsstsMain.py file:
    1.  Import your Python file.
    2.  Add an entry to the GUI, which you can later select. 
    3.  Each selected test adds a scheme to a list, which includes all tests that will be executed. In case your schedulability test gets selected, you need to add your scheme, so that the algorithm is later called.
    4.  Set a text for the label, so that the name of your test will be displayed in the GUI
    5.  At an additional case to the switchTest method, which will select and execute your schedulability test, if you added your scheme correctly.
* In order to make the implementation easier, you can search for an existing implementation, for example 'RSS' and copy each step to implement your own algorithm. 

## Acknowledgements

We would like to thank all the authors who helped to extend the framework. In particular, we would like to thank Bo Peng, Morteza Mohaqeqi, Alessandro Biondi and Beyazit Yalcinkaya for providing the source code and additonal information of their work.
