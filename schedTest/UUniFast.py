from __future__ import division
import random
import math
import sys, getopt
import json
import tgPath
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np



fig = plt.figure()
axx = fig.add_subplot(111, projection='3d')


USet=[]
PSet=[]   

def UUniFast(n,U_avg):
  global USet
  sumU=U_avg
  for i in range(n-1):
    nextSumU=sumU*math.pow(random.random(), 1/(n-i))    
    USet.append(sumU-nextSumU)
    sumU=nextSumU
  USet.append(sumU)

ax=[]
ay=[]
az=[]

for i in range(0, 1000, 1):                  
    tasks = tgPath.taskGeneration_p(3, 100,0.01,0.1, vRatio=1, seed=i, numLog=2, numsegs=2)
    ax.append(math.ceil(tasks[0]['utilization']))
    ay.append(math.ceil(tasks[1]['utilization']))
    az.append(math.ceil(tasks[2]['utilization']))
axx.scatter(ax, ay, az, c='r', marker='1', )
axx.view_init(20, 45)

axx.set_xlabel('X Label')
axx.set_ylabel('Y Label')
axx.set_zlabel('Z Label')
fig.savefig('UUniFast.pdf', bbox_inches='tight')
#plt.show()