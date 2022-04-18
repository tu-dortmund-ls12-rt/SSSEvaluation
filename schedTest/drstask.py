from __future__ import division
import random
import math
import sys, getopt
import json
import datetime
from drs import drs


DRS_exe=[]
DRS_val=[]
PSet=[]


def DRS_WCET(n, util=1):
  
   global DRS_exe

   DRS_exe = drs(n, util)



def CSet_generate(Pmin,numLog):
    j=0
    global PSet

    for i in DRS_exe:
    
       thN=j%1
       p=random.uniform(100*math.pow(10, thN), 100*math.pow(10, thN+1))
       pair={}
       pair['period']=p
       pair['execution']=i*p

       #multiplying period with first utilization values to generate WCET

       pair['deadline']=p
       pair['utilization']=i
       PSet.append(pair)
       j=j+1
       


def suspend(Pmin, numLog):
   j=0
   global PSet

   for i in DRS_val:
       thN=j%1
       p=random.uniform(100*math.pow(10, thN), 100*math.pow(10, thN+1))
       pair={}
       pair['period']=p
       pair['sslength']=i*p

       #multiplying period with the other utilization values to generate the suspension time

       PSet.append(pair)
       j=j+1
       
   return PSet



def taskGeneration_drs(NumberOfTasksPerSet,uTotal,u_Bound,l_Bound,minsslength,maxsslength,Pmin=100, numLog=1):

   global DRS_val 

   DRS_WCET(NumberOfTasksPerSet, uTotal)

   DRS_val = drs(NumberOfTasksPerSet, uTotal, u_Bound, l_Bound)
    
   CSet_generate(Pmin,numLog)
    
   suspend(Pmin,numLog)

   return PSet
