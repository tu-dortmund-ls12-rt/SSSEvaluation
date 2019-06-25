# Evaluation Framework for Self-Suspending Task Systems
This tutorial explains how to use the framework discussed in the paper:
>Georg von der Brüggen, Milad Nayebi, Junjie Shi, Kuan-Hsun Chen, and Jian-Jia Chen, Evaluation Framework for Self-Suspending Task Systems, 10th International Workshop on Analysis Tools and Methodologies for Embedded and Real-time Systems (WATERS 2019), to appear, July 2019

Our goal is to provide an easy to use framework that allows to compare these schedulability tests based on synthesized task sets.

We consider three Self-Suspending Task models:
1. The segmented model, where the self-suspension behaviour is described by a precise pattern of interleaving execution segments and suspension intervals.
2. The dynamic model, where the self-suspension behaviour is described by two upper bounds on the total worst-case execution time (WCET) and the total suspension time. It assumes that a task can suspend itself an infinity amount of times as long as the upper bound on the total suspension time is respected.
3. The hybrid models, that provide different tradeoffs between the overly flexible dynamic model and the overly restrictive segmented model, assuming different levels of information in addition to the bounds on WCET and suspension time, i.e., at least the number of suspensions.

We also want to include MILP solvers like http://retis.sssup.it/~a.biondi/ae/FRED/ in the near future.

# Framework Introduction

The provided Python framework evaluates scheduling algorithms and the related schedulability tests based on randomly generated implicit-deadline task sets. The evaluation setup can be configured using multiple parameters like the number of tasks, the utilization range that is considered, the relative length of the suspension interval, the number of sets per configuration, etc. 

Furthermore, it is also possible to configure the evaluation setup of the framework using a config file, running it based on a command line. The results of the tests are stored in numpy files and can also directly be printed into pdfs. The framework also supports to plot previously collected data. 

The framework already includes schedulability tests for multiple algorithms:
* SEIFDA: Georg von der Brüggen, Wen-Hung Huang, Jian-Jia Chen, and Cong Liu. Uniprocessor scheduling strategies for self-suspending task systems. In RTNS 2018.
* SCAIR: Lea Schonberger, Wen-Hung Huang, Georg von der Brüggen, Kuan-Hsun Chen, and Jian-Jia Chen. Schedulability analysis and priority assignment for segmented self-suspending tasks. In RTCSA 2018.
* PASS: Wen-Hung Huang, Jian-Jia Chen, Husheng Zhou, and Cong Liu. PASS: Priority assignment of real-time tasks with dynamic suspending behavior under fixed-priority scheduling. In DAC 2015.

# Framework Usage
![GUI of the framework](https://github.com/tu-dortmund-ls12-rt/SSSEvaluation/blob/master/framework_gui-1.jpg)
