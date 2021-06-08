# Evaluation Framework for Self-Suspending Task Systems
This tutorial explains how to use the framework discussed in the paper:
>Georg von der Brüggen, Milad Nayebi, Junjie Shi, Kuan-Hsun Chen, and Jian-Jia Chen, Evaluation Framework for Self-Suspending Task Systems, 10th International Workshop on Analysis Tools and Methodologies for Embedded and Real-time Systems (WATERS 2019), July 2019

Our goal is to provide an easy to use framework that allows to compare these schedulability tests based on synthesized task sets.

We consider three Self-Suspending Task models:
1. The segmented model, where the self-suspension behaviour is described by a precise pattern of interleaving execution segments and suspension intervals.
2. The dynamic model, where the self-suspension behaviour is described by two upper bounds on the total worst-case execution time (WCET) and the total suspension time. It assumes that a task can suspend itself an infinity amount of times as long as the upper bound on the total suspension time is respected.
3. The hybrid models, that provide different tradeoffs between the overly flexible dynamic model and the overly restrictive segmented model, assuming different levels of information in addition to the bounds on WCET and suspension time, i.e., at least the number of suspensions.

We have included Alessandros Method. Biondi (RTSS 2016) like http://retis.sssup.it/~a.biondi/ae/FRED/.
The modifed version is compress as a tar file named as RTSS-modifed.tar. Please follow the original instructions to install relative libraries, modify the Makefile path and build the executable binary.

# Framework Introduction

The provided Python framework evaluates scheduling algorithms and the related schedulability tests based on randomly generated implicit-deadline task sets. The evaluation setup can be configured using multiple parameters like the number of tasks, the utilization range that is considered, the relative length of the suspension interval, the number of sets per configuration, etc. 

Furthermore, it is also possible to configure the evaluation setup of the framework using a config file, running it based on a command line. The results of the tests are stored in numpy files and can also directly be printed into pdfs. The framework also supports to plot previously collected data. 

The framework already includes schedulability tests for multiple algorithms:
* SEIFDA: Georg von der Brüggen, Wen-Hung Huang, Jian-Jia Chen, and Cong Liu. Uniprocessor scheduling strategies for self-suspending task systems. In RTNS 2018.
* SCAIR: Lea Schonberger, Wen-Hung Huang, Georg von der Brüggen, Kuan-Hsun Chen, and Jian-Jia Chen. Schedulability analysis and priority assignment for segmented self-suspending tasks. In RTCSA 2018.
* PASS: Wen-Hung Huang, Jian-Jia Chen, Husheng Zhou, and Cong Liu. PASS: Priority assignment of real-time tasks with dynamic suspending behavior under fixed-priority scheduling. In DAC 2015.

# Framework Usage
![GUI of the framework](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/framework_gui-2.jpg)

# How to integrate your algorithms?

The framework can be extended with other scheduling algorithms written in Python or C++. The integration is in twofold:
* Make sure the content of task is consistent to your existed algorithms. This is a bit tricky: Each task is formed as a dictionary in Python, which consists of its period ['period'], worst case execution time ['execution'], utilization ['utilization'], relative deadline ['deadline'], the possible suspension time ['sslength'], the set of execution segements ['Cseg'], the set of suspension segements ['Sseg']. For the other keys in the dictionary, they are the intermediate variables for task generations.
* Based on the same format of tasks, the targeted algorithm in Python should be implemented accordingly (recommended to store in the folder of schedTest). If the algorithm is written in C++, an executable binary needs to be pre-built so that the process can be called from the main python script. The properties of tasks and the result of the analysis are transmitted in the form of csv or txt file.

# Framework Installation

##Requirements

The following software should be installed:
```
sudo apt-get install git python3
pip install PyQt5 numpy mip gurobipy matplotlib
```

To activate the full feature set of the framework, you also need to install the Gurobi Optimizer, found at https://www.gurobi.com/. For research purposes you can obtain an academic license, which is used for some of the scheduling algorithms. You can request a license at https://www.gurobi.com/academia/academic-program-and-licenses/. The installation guide can be found at https://www.gurobi.com/documentation/9.1/quickstart_linux/software_installation_guid.html.

## File Structure

    .
    ├── effsstsPlot			# Placeholder for outputs
    │   ├── Data			# Includes all output graphs
    │   └── effsstsPlot.py		# Output graph generation
    ├── schedTest			# Contains all schedulability tests
    │   ├── inputs			# Temporary Inputs for schedulability tests
    │   └── temp_models		# Temporary models for schedulability tests
    ├── effssts.py			# Framework executable without GUI
    ├── effsstsMain.py			# Framework executable with GUI
    ├── gurobi.env			# Settings for Gurobi optimizer
    ├── README.md
    
## Deployment

The following steps explain how to deploy this framework on the machine:

First, clone the git repository or download the [zip file](https://github.com/tu-dortmund-ls12-rt/end-to-end/archive/refs/heads/master.zip):
```
git clone https://github.com/tu-dortmund-ls12-rt/SSSEvaluation.git
```
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
    
# Schedulability Tests

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

# Acknowledgements

We would like to thank all the authors who helped to extend the framework. In particular, we would like to thank Bo Peng, Morteza Mohaqeqi, Alessandro Biondi and Beyazit Yalcinkaya for providing the source code and additonal information of their work.
