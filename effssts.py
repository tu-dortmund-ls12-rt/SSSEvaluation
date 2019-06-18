from __future__ import division
import random
import sys
import getopt
import numpy as np
from schedTest import tgPath, SCEDF, EDA, PROPORTIONAL, NC, SEIFDA, Audsley, rad, PATH, mipx
from effsstsPlot import effsstsPlot
import os
import datetime
import ConfigParser as cp



def readParameters():
	args = sys.argv

	config = cp.RawConfigParser()
	config.read(args[1])

	global prefixdata
	global runtest
	global plotdata
	global totBucket
	global tasksinBkt
	global UStart
	global UEnd
	global UStep
	global ssofftypes
	global schemes
	# global sstype
	global minsstype
	global maxsstype
	global plotall

	prefixdata = config.get('General', 'prefixdatapath')
	runtest = config.getboolean('General', 'runtest')
	plotdata = config.getboolean('General', 'plotdata')
	plotall = config.getboolean('General', 'plotall')

	totBucket = config.getint('Tasks', 'totalbucket')
	tasksinBkt = config.getint('Tasks', 'taskinbucket')
	UStart = config.getint('Tasks', 'utilizationstart')
	UEnd = config.getint('Tasks', 'utilizationend')
	UStep = config.getint('Tasks', 'utilizationstep')

	ssofftypes = config.getint('Tasks', 'numberofsegments')

	schemes = []
	tempSchemes = config.get('Schedulability Tests', 'schemes').split(',')
	for scheme in tempSchemes:
		schemes.append(scheme.strip())

	minsstype = float(config.get('Suspension Length', 'minsslength'))
	maxsstype = float(config.get('Suspension Length', 'maxsslength'))

def main():
	sspropotions=['10']
	periodlogs=['2']
	for ischeme in schemes:
		for issprop in sspropotions:
			for iplog in periodlogs:							
				# Initialize X and Y axes 
				x = np.arange(0, int(100/UStep)+1) 
				y = np.zeros(int(100/UStep)+1)
				ifskip=False
				for u in xrange(0,len(y),1):
					print "Scheme:",ischeme,"N:",totBucket,"U:",u*UStep, "MinSSLength:",str(minsstype), "MaxSSLength:",str(maxsstype),"OffType:",ssofftypes,"prop: ", issprop
					if u == 0:
						y[u] = 1
						continue
					if u*UStep == 100:
						y[u] = 0
						continue
					numfail = 0
					if ifskip == True:
						print "acceptanceRatio:", 0
						y[u] = 0
						continue 

					for i in xrange(0, totBucket, 1):									
						percentageU = u*UStep/100
						prop = int(issprop)/10
						tasks = tgPath.taskGeneration_p(tasksinBkt, percentageU,minsstype,maxsstype, vRatio=prop, seed=i, numLog=int(iplog), numsegs=ssofftypes)
						sortedTasks=sorted(tasks, key=lambda item:item['period'])

						if ischeme == 'SCEDF':
							if SCEDF.SC_EDF(tasks) == False:
								numfail+=1
						elif ischeme == 'SCRM':
							if SEIFDA.SC_RM(tasks) == False:
								numfail+=1
						elif ischeme == 'PASS-OPA':
							if Audsley.Audsley(tasks) == False:
								numfail+=1								
						elif ischeme == 'MIP':
							if mipx.mip(tasks) == False:
								numfail+=1								
						elif ischeme.split('-')[0] == 'SEIFDA':
							if SEIFDA.greedy(tasks,ischeme) == False:
								numfail+=1
						elif ischeme.split('-')[0] == 'PATH':
							if PATH.PATH(tasks,ischeme) == False:
								numfail+=1
						elif ischeme == 'EDA':
							if EDA.EDA(tasks, ssofftypes) == False:								
								numfail+=1
						elif ischeme == 'PROPORTIONAL':
							if PROPORTIONAL.PROPORTIONAL(tasks, ssofftypes) == False:								
								numfail+=1
						elif ischeme == 'NC':
							if NC.NC(tasks) == False:										
								numfail+=1
						elif ischeme == 'SCAIR-RM':
							if rad.scair_dm(tasks) == False:
								numfail+=1
						elif ischeme == 'SCAIR-OPA':
							if rad.Audsley(sortedTasks,ischeme) == False:
								numfail+=1
						else:
							assert ischeme, 'not vaild ischeme'
			
					acceptanceRatio=1-(numfail/totBucket)
					print "acceptanceRatio:",acceptanceRatio
					y[u]=acceptanceRatio
					if acceptanceRatio == 0:
						ifskip=True
				
				plotPath = prefixdata + '/' + str(minsstype) + '-' + str(maxsstype) + '/' + str(ssofftypes) + '/'
				plotfile = prefixdata + '/' + str(minsstype) + '-' + str(maxsstype) + '/' + str(ssofftypes) + '/' + ischeme# + '-' + datetime.datetime.now().strftime('%Y%m%d%H%M%S')

				if not os.path.exists(plotPath):
					os.makedirs(plotPath)
				
				np.save(plotfile,np.array([x,y]))
				#effsstsPlot.effsstsPlot(ischeme)

def usage():
	howToUse = """
	######## ######## ########  ######   ######  ########  ######
	##       ##       ##       ##    ## ##    ##    ##    ##    ##
	##       ##       ##       ##       ##          ##    ##
	######   ######   ######    ######   ######     ##     ######
	##       ##       ##             ##       ##    ##          ##
	##       ##       ##       ##    ## ##    ##    ##    ##    ##
	######## ##       ##        ######   ######     ##     ######
																
	--------------------------------------------------------------
	USAGE:
	--------------------------------------------------------------

	python effssts.py [configuration file]

	--------------------------------------------------------------
	STRUCTURE OF CONFIGURATION FILE:
	--------------------------------------------------------------

	[General]
	prefixdatapath = effsstsPlot/datart4
	runtest = true
	plotdata = true
	plotall = true

	[Tasks]
	totalbucket = 100
	taskinbucket = 5
	utilizationstart = 0
	utilizationend = 100
	utilizationstep = 5
	numberofsegments = 3

	[Suspension Length]
	#UB = task['period'] - task['execution']
	#Short = random.uniform(0.01*UB,0.1*UB)
	#Moderate = random.uniform(0.1*UB,0.3*UB)
	#Long = random.uniform(0.3*UB,0.6*UB)
	minsslength = 0.10
	maxsslength = 0.40

	[Schedulability Tests]
	schemes = SCAIR-OPA, EDA
	"""
	print howToUse
if __name__ == '__main__':
	args = sys.argv
	if len(args) < 2:
		usage()
	else:
			readParameters()
			if runtest:
				main()
			if plotdata:
				effsstsPlot.effsstsPlotAll(prefixdata, plotall, schemes, minsstype, maxsstype, ssofftypes, UStart, UEnd, UStep, tasksinBkt)