from __future__ import division
import random
import math
import sys, getopt
import json
import datetime
from drs import drs

DRS_exe=[]
DRS_val=[]
Task=[]


def Period_generate(Pmin, numLog):                      #generating 10 tasks..
    
   j=0
   
   global DRS_exe, DRS_val, p 
   temp = 0
   for i in DRS_exe:
           
       thN=j%1 
       p=random.uniform(100*math.pow(10, thN), 100*math.pow(10, thN+1))
       pair={}
       pair['period']=p
       pair['execution']=i*p
       pair['suspension']=p*DRS_val[temp]
       Task.append(pair)
       temp = temp + 1
       j=j+1

   
   return Task


def DRS_wcet(n, util=1):                                #generating 10 utilization values <=1
     
   global DRS_exe

   DRS_exe = drs(n, util)
   
   
     
def DRS_sus(n, util, ubound, lbound):                             #generating other 10 utils
    
    global DRS_val
    
    DRS_val = drs(n, util, ubound, lbound)
    
      

def taskGeneration_drs(NumberOfTasksPerSet,uTotal,u_Bound,l_Bound,minsslength,maxsslength,Pmin=100,numLog=1):

   DRS_wcet(NumberOfTasksPerSet, uTotal)
   
   DRS_sus(NumberOfTasksPerSet,uTotal,u_Bound,l_Bound)

   Period_generate(Pmin,numLog)
   
   print('number of tasks:', len(Task))
   
   return Task