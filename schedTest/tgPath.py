from __future__ import division
import random
import math
import sys, getopt
import json
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

def UUniFast_Discard(n,U_avg):
	while 1:
		sumU=U_avg
		for i in range(n-1):
			nextSumU=sumU*math.pow(random.random(), 1/(n-i))
			USet.append(sumU-nextSumU)
			sumU=nextSumU
		USet.append(sumU)

		if max(USet) < 1:
			break
		del USet[:]

def ExpDist(limit,U_mean):
	while 1:
		uBkt=random.expovariate(U_mean)
		print(uBkt)
		if sum(taskSet) + uBkt > limit:
			break
		taskSet.append(uBkt)
def UniDist(n,U_min,U_max):
	for i in range(n-1):
		uBkt=random.uniform(U_min, U_max)
		taskSet.append(uBkt)
def CSet_generate(Pmin,numLog):
	global USet,PSet
	j=0
	for i in USet:
		thN=j%numLog
		p=random.uniform(Pmin*math.pow(10, thN), Pmin*math.pow(10, thN+1))
		pair={}
		pair['period']=p
		pair['execution']=i*p
		pair['deadline']=p
		pair['utilization']=i
		PSet.append(pair)
		j=j+1

def seg_UUniFast(n,total):
	seg=[]
	sumU=total
	for i in range(n-1):
		nextSumU=sumU*math.pow(random.random(), 1/(n-i))
		seg.append(sumU-nextSumU)
		sumU=nextSumU
	seg.append(sumU)

	return seg
def SSS_seg_gen(vRatio,minCtune,maxCtune,maxnumsegs,minSratio,numpaths,scalef):
	global PSet
	numV=int(len(PSet)*vRatio)
	i=0

	for itask in PSet:
		if i< numV:
			UB=itask['period']-itask['execution']
			s=random.uniform(minCtune*UB,maxCtune*UB)

			itask["sslength"]=s

			itask["minSr"]=minSratio
			itask["paths"]=[]
			itask["Cseg"]=[]
			itask["Sseg"]=[]
			#the path with the maximum C
			#the path with the maximum S
			iMaxE=random.randrange(numpaths)
			iMaxS=random.randrange(numpaths)
			maxSumC=0
			maxSumS=0
			#generate each path
			for j in range(numpaths):


				path={}

				if j!=iMaxE:
					path["Cseg"]=seg_UUniFast(maxnumsegs,itask['execution']*random.uniform(scalef,1))
				else:
					path["Cseg"]=seg_UUniFast(maxnumsegs,itask['execution'])

				if j!=iMaxS:
					path["Sseg"]=seg_UUniFast(maxnumsegs-1,itask['sslength']*random.uniform(scalef,1))
				else:
					path["Sseg"]=seg_UUniFast(maxnumsegs-1,itask['sslength'])

				deadlineD=[]
				for k in range(len(path['Cseg'])):
					deadlineD.append(-1)
				path['deadline']=deadlineD
				##integeraize
				sumC=0
				sumS=0
				for k in range(len(path['Cseg'])):
					path['Cseg'][k]=max(1,int(path['Cseg'][k]))
					sumC+=path['Cseg'][k]
				for k in range(len(path['Sseg'])):
					path['Sseg'][k]=max(1,int(path['Sseg'][k]))
					sumS+=path['Sseg'][k]

				itask["paths"].append(path)
				if sumC>maxSumC:
					maxSumC=sumC
				if sumS>maxSumS:
					maxSumS=sumS

			for j in range(maxnumsegs):
				maxCseg=0
				for k in range(numpaths):
					if itask["paths"][k]["Cseg"][j]>maxCseg:
						maxCseg=itask["paths"][k]["Cseg"][j]
				itask["Cseg"].append(maxCseg)


			for j in range(maxnumsegs-1):
				maxSseg=0
				for k in range(numpaths):
					if itask["paths"][k]["Sseg"][j]>maxSseg:
						maxSseg=itask["paths"][k]["Sseg"][j]

				itask["Sseg"].append(maxSseg)



			itask['period']=math.ceil(itask['period'])
			itask['execution']=maxSumC
			itask['sslength']=maxSumS

		else:
			s=0
			itask["sslength"]=s

		i+=1
def init():
	global USet,PSet
	USet=[]
	PSet=[]

def taskGeneration_p(numTasks,uTotal,minsslength,maxsslength,Pmin=100,numLog=1,vRatio=1,seed=1,numsegs=2,minSratio=1,numpaths=2,scalef=0.8):
    init()
    #random.seed() This is called before this function is called
    UUniFast(numTasks,uTotal)
    CSet_generate(Pmin,numLog)
    SSS_seg_gen(vRatio,minsslength,maxsslength,numsegs,minSratio,numpaths,scalef)
    return PSet


