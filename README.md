# Evaluation Framework for Self-Suspending Task Systems

The provided Python framework evaluates scheduling algorithms and the related schedulability tests based on randomly generated implicit-deadline task sets. The evaluation setup can be configured using multiple parameters like the number of tasks, the utilization range that is considered, the relative length of the suspension interval, the number of sets per configuration, etc..

An overview of the framework can be found in this [paper](https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/WATERS_2019_paper_8.pdf):
>Georg von der Brüggen, Milad Nayebi, Junjie Shi, Kuan-Hsun Chen, and Jian-Jia Chen, Evaluation Framework for Self-Suspending Task Systems, 10th International Workshop on Analysis Tools and Methodologies for Embedded and Real-time Systems (WATERS 2019), July 2019 

Our goal is to provide an easy to use evaluation framework with a pre-implemented task generator, some pre-implemented schedulability tests, and an integrated plotting tool to compare these schedulability tests under the same conditions.

This framework support the Self-Suspending Task models:
1. The segmented model, where the self-suspension behaviour is described by a precise pattern of interleaving execution segments and suspension intervals.
2. The dynamic model, where the self-suspension behaviour is described by two upper bounds on the total worst-case execution time (WCET) and the total suspension time. It assumes that a task can suspend itself an infinity amount of times as long as the upper bound on the total suspension time is respected.
3. The hybrid models, that provide different tradeoffs between the overly flexible dynamic model and the overly restrictive segmented model, assuming different levels of information in addition to the bounds on WCET and suspension time, i.e., at least the number of suspensions.#

![GUI of the framework](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/framework_gui-2.jpg)

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
pip install PyQt5 numpy mip gurobipy matplotlib
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

After that you can select the parameters for the task set in the **Configuration** tab. This includes the number of tasks per set, the number of task sets, the utilization values, the number of computation segments, and the ratio between computation and suspension time.

In the **Schedulability tests** tab you can select any of the schedulability tests which are implemented in the framework. Additionally you can set custom parameters for some of the tests.

After that, the **Plots** tab lets you specify how to plot the schedulability tests. You can plot each test individually, combine all selected tests or combine available tests, if they were previously plotted and their data is available in the **effsstsPlot/Data/\*** folder.

After running the schedulability analysis, you can find the results in the **effsstsPlot/Data** folder.

## Implementation Details

To create the task sets, we use the UUnifast algorithm, which is used to generate the utilizations of each task. Each task set includes every information needed for the segmented, dynamic and hybrid task model and are generated as follows:

1. For the dynamic model, the user specifies the suspension ratio, so that after generating the utilization, the total execution and suspension time are included in the task.

2. For the dynamic model, we generate different execution and suspension times for each task as individual paths and then include the upper bound of each computation and suspension segment in the task.

3. For the hybrid model, the task includes the maximum execution and suspension time, aswell as the number of computation and suspension segments.

## Schedulability Tests

Name | Paper | File name | Method name
---|---|---|---
SEIFDA-minD- | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-maxD- | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-PBminD- | https://dl.acm.org/doi/10.1145/2997465.2997497 | SEIFDA.py | SEIFDA
SEIFDA-MILP | https://dl.acm.org/doi/10.1145/2997465.2997497 | mipx.py | mip
EDA | | EDA.py | SEIFDA
PROPORTIONAL | | PROPORTIONAL.py | PROPORTIONAL
GMFPA | https://link.springer.com/article/10.1007/s11241-017-9279-2 | GMFPA.py | GMFPA
Oblivious-IUB | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Clairvoyant-SSSD | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Oblivious-MP | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
Clairvoyant-PDAB | https://ieeexplore.ieee.org/abstract/document/8046328 | PATH.py | SEIFDApath
SCEDF | https://link.springer.com/content/pdf/10.1007/s11241-018-9316-9.pdf Section 7.1 | SCEDF.py | SC_EDF
SCRM | https://link.springer.com/content/pdf/10.1007/s11241-018-9316-9.pdf Section 4.2.4 | SCRM.py | SC_RM
SCAIR-RM | https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2015-technical-report-multi-seg-Kevin.pdf | rad.py | scair_dm
SCAIR-OPA | https://ls12-www.cs.tu-dortmund.de/daes/media/documents/publications/downloads/2015-technical-report-multi-seg-Kevin.pdf | rad.py | Audsley
Biondi RTSS 16 | https://ieeexplore.ieee.org/document/7176028 | Biondi.py | Biondi
PASS-OPA | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7167340 | Audsley.py | Audsley
NC | | NC.py | NC
RSS | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Section V | RSS.py | SC2EDF
UDLEDF | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Section III | UDLEDF.py | UDLEDF_improved
WLAEDF | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Section III | WLAEDF.py | WLAEDF
RTEDF  | https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9211430 Algorithm1 | RTEDF.py | RTEDF
Uniframework | https://ieeexplore.ieee.org/abstract/document/7557869 Section V | UNIFRAMEWORK.py | UniFramework
SuspObl | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspObl
SuspJit | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspJit
SuspBlock | https://ieeexplore.ieee.org/abstract/document/7557869 Section III | FixedPriority.py | SuspBlock
GMF-PA | https://link.springer.com/article/10.1007/s11241-017-9279-2 | GMFPA.py | GMFPA
SRSR | https://dl.acm.org/doi/abs/10.1145/2997465.2997485 | SRSR.py | SRSR

## File Structure
    .
    ├── effsstsPlot	
    │   ├── Data			# Includes all output graphs
    │   └── effsstsPlot.py		# Output graph generation
    ├── schedTest			# Contains all schedulability tests
    │   ├── inputs			# Temporary Inputs for schedulability tests
    │   └── temp_models		# Temporary models for schedulability tests
    ├── effssts.py			# Framework executable without GUI
    ├── effsstsMain.py			# Framework executable with GUI
    ├── gurobi.env			# Settings for Gurobi optimizer
    ├── README.md
    
## How to integrate your algorithms?

The framework can be extended with other scheduling algorithms written in Python or C++. The integration is in twofold:
* Make sure the content of task is consistent to your existed algorithms. This is a bit tricky: Each task is formed as a dictionary in Python, which consists of its period ['period'], worst case execution time ['execution'], utilization ['utilization'], relative deadline ['deadline'], the possible suspension time ['sslength'], the set of execution segements ['Cseg'], the set of suspension segements ['Sseg']. For the other keys in the dictionary, they are the intermediate variables for task generations.
* Based on the same format of tasks, the targeted algorithm in Python should be implemented accordingly (recommended to store in the folder of schedTest). If the algorithm is written in C++, an executable binary needs to be pre-built so that the process can be called from the main python script. The properties of tasks and the result of the analysis are transmitted in the form of csv or txt file.

## Acknowledgements
We would like to thank all the authors who helped to extend the framework. In particular, we would like to thank Bo Peng, Morteza Mohaqeqi, Alessandro Biondi and Beyazit Yalcinkaya for providing the source code and additonal information of their work.
