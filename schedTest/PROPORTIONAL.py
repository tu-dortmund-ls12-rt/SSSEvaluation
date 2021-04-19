from __future__ import division
import random
import math
import sys, getopt
import json
from schedTest import functions

def dbfProportional(t,task,ssofftypes):
  sum=0
  for i in range(ssofftypes):
    sum+=task['Cseg'][i]

  #D=(task['period']-task['sslength'])/ssofftypes

  TiMinusSi=0
  for i in range(ssofftypes):
    TiMinusSi+=task['Cseg'][i]/sum

  if t<TiMinusSi:
    return 0
  else:
    return sum+ math.floor(((t-(TiMinusSi))/task['period']))*sum

  
def PROPORTIONAL(tasks, ssofftypes):
  sortedTasks=sorted(tasks,key= lambda x: functions.lm_cmp(x))
  for i in range(len(sortedTasks)):
    task=sortedTasks[i]
    Ci=0
    for j in range(ssofftypes):
      Ci+=task['Cseg'][j]
    D = 0
    # for k in range(ssofftypes):
    #   D+=(task['Cseg'][k])/Ci
    #D=(task['period']-task['sslength'])/ssofftypes
    #D=(task['period']-task['sslength'])*task['Cseg'][1]/Ci
    D = ((task['Cseg'][ssofftypes-1])/Ci)*(task['period']-task['sslength'])
    dbf=0
    HEPTasks=sortedTasks[:i+1]
    for jtask in HEPTasks:
      dbf+=dbfProportional(D,jtask,ssofftypes)
    if dbf>D:
      return False
  return True