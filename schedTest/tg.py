from __future__ import division
import random
import math
import sys
import datetime

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


def	SetGenerate(Pmin,numLog):
	global USet,PSet
	j=0
	for i in USet:
		thN=j%numLog
		p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
		pair={}
		pair['period']=p
		pair['execution']=i*p
		PSet.append(pair)
		j=j+1

def segUUniFast(n,total):
	seg=[]
	sumU=total
	for i in range(n-1):
		nextSumU=sumU*math.pow(random.random(), 1/(n-i))
		seg.append(sumU-nextSumU)
		sumU=nextSumU
	seg.append(sumU)

	return seg
def SSSetGenerate(vRatio,minCtune,maxCtune,maxnumsegs):
	global PSet
	numV=int(len(PSet)*vRatio)
	i=0

	for itask in PSet:
		if i< numV:
			UB=itask['period']-itask['execution']
			s=random.uniform(minCtune*UB,maxCtune*UB)

			itask["sslength"]=s
			#numsegs=random.randrange(2,maxnumsegs)

			#itask["Cseg"]=segUUniFast(numsegs,itask['execution'])
			#itask["Sseg"]=segUUniFast(numsegs-1,itask['sslength'])\

			itask["Cseg"]=segUUniFast(maxnumsegs,itask['execution'])
			itask["Sseg"]=segUUniFast(maxnumsegs-1,itask['sslength'])
			csum=0
			ssum=0
			for j in range(len(itask['Cseg'])):
				csum+=max(1,int(itask['Cseg'][j]))
				itask['Cseg'][j]=max(1,int(itask['Cseg'][j]))
			for j in range(len(itask['Sseg'])):
				ssum+=max(1,int(itask['Sseg'][j]))
				itask['Sseg'][j]=max(1,int(itask['Sseg'][j]))
			itask['period']=math.ceil(itask['period'])
			itask['execution']=csum
			itask['sslength']=ssum

		else:
			s=0
			itask["sslength"]=s
			itask['peroid']=math.ceil(itask['peroid'])
			itask['execution']=max(1,int(itask['execution']))


		i+=1
def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration_p(numTasks,uTotal,Pmin=10,numLog=2,vRatio=1,sstype="M",seed=1,offtype="R"):
        if seed = 9999:
    	    random.seed(datetime.datetime.now())
	init()
	minCtune=0.1
	maxCtune=0.6
	numsegs=2
	#parameterRead()
	if sstype == 'M':
		minCtune=0.1
		maxCtune=0.3
	elif sstype == 'S':
		minCtune=0.01
		maxCtune=0.1
	elif sstype == 'L':
		minCtune=0.3
		maxCtune=0.6
	else:
		assert "error"
		sys.exit()

	if offtype == 'R':
		numsegs=2
	elif offtype == 'M':
		numsegs=5
	elif offtype == 'F':
		numsegs=10
	else:
		assert "error"
		sys.exit()

	## the UUniFast method is adopted to generate a set of utilization values with the given goal
	UUniFast(numTasks,uTotal)
	## generate the task periods according to the log distribution
	SetGenerate(Pmin,numLog)
	## converted sporadic tasks to suspension tasks
	SSSetGenerate(vRatio,minCtune,maxCtune,numsegs)

	return PSet

