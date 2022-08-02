from __future__ import division
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import sys
import numpy as np
from schedTest import drstask, Burst_RM, tgPath, SCEDF, SCRM, EDA, PROPORTIONAL, NC, SEIFDA, pass_opa, rad, PATH, mipx, scair_rm
from schedTest import RSS, UDLEDF, WLAEDF, RTEDF, UNIFRAMEWORK, FixedPriority, GMFPA, SRSR, milp_response, UPPAAL, Burst_RM
from effsstsPlot import effsstsPlot
import os
import datetime
import pickle
from multiprocessing import Pool
from pathlib import Path

gEx = 1
gEx_Sus = 2
gNumberOfTasksPerSet = 10
uTotal = 1
minsslength = 0.01
maxsslength = 0.10


def ufast():

	tasks = tgPath.taskGeneration_p(gNumberOfTasksPerSet,uTotal,minsslength,maxsslength,Pmin=100,numLog=1,vRatio=1,seed=1,numsegs=2,minSratio=1,numpaths=2,scalef=0.8)

	return tasks

tasksets_ufast = ufast()  #

def drs():
	tasks_drs = drstask.taskGeneration_drs(gNumberOfTasksPerSet, gEx_Sus, gEx, Pmin=100, numLog=1)

	return tasks_drs 

tasksets_drs = drs()


print('UUniFast:',tasksets_ufast)

print('DRS:',tasksets_drs)



sus_obv = FixedPriority.SuspJit(tasksets_ufast)

#sus_obv_drs = FixedPriority.SuspObl(tasksets_drs)

print(sus_obv)

#print(sus_obv_drs)


sus_jit = FixedPriority.SuspJit(tasksets_ufast)

#sus_jit_drs = FixedPriority.SuspJit(tasksets_drs)

print(sus_jit)

#print(sus_jit_drs)




