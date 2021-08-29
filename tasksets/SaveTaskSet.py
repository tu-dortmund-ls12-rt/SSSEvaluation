import pickle
import pathlib
import csv
import json

print("Please enter number of task sets (Ts)")
gNumberOfTaskSets = int(input())
print("Please enter number of tasks per task sets (Tn)")
gNumberOfTasksPerSet = int(input())
print("Please enter utilization start value (gUStart)")
gUStart = int(input())
print("Please enter utilization end value (gUEnd)")
gUEnd = int(input())
print("Please enter utilization step value (gUStep)")
gUStep = int(input())
print("Please enter minimum suspension length")
gSLenMinValue = float(input())
print("Please enter maximum suspension length")
gSLenMaxValue = float(input())
print("Please enter number of computation segments")
gNumberOfSegs = int(input())
print("Please enter seed for randomizer")
gSeed = int(input())
print("Please enter the file name from the Input folder (including .csv) containing the task information. You can find a description of the data layout in the Input folder.")
input_file_name = input()

info = [gNumberOfTaskSets, gNumberOfTasksPerSet, gUStep, gUStart, gUEnd, gSLenMinValue, gSLenMaxValue, gNumberOfSegs, gSeed ]

file_name = 'Ts-'+ str(gNumberOfTaskSets) + '-Tn-' \
			+ str(gNumberOfTasksPerSet) + '-Ust-' + str(gUStep) +\
			'-Ssl-' + str(gSLenMinValue) + '-' + \
			str(gSLenMaxValue) + '-Seg-'+str(gNumberOfSegs)+'-.pkl'

tasksets_utils = []

with open(str(pathlib.Path(__file__).parent.absolute())+'/input/'+input_file_name, 'r') as file:
	reader = csv.DictReader(file)
	for utilization in range(gUStart,gUEnd+1,gUStep):
		utilization = []
		for taskset in range(gNumberOfTaskSets):
			taskset = []
			for task in range(gNumberOfTasksPerSet):
				task = next(reader)
				task['period'] = int(task['period'])
				task['execution'] = int(task['execution'])
				task['deadline'] = int(task['deadline'])
				task['utilization'] = float(task['utilization'])
				task['sslength'] = int(task['sslength'])
				task['minSr'] = int(task['minSr'])
				task['paths'] = json.loads(task['paths'].replace("'", '"')) 
				task['Cseg'] = list(map(int, task['Cseg'][1:-1].split(",")))
				task['Sseg'] = list(map(int, task['Sseg'][1:-1].split(",")))
				taskset.append(task)
			utilization.append(taskset)
		tasksets_utils.append(utilization)

with open(str(pathlib.Path(__file__).parent.absolute())+'/saves/'+file_name, 'wb') as f:
	pickle.dump([tasksets_utils,info] , f)
	
print("Task sets saved at "+str(pathlib.Path(__file__).parent.absolute())+'/saves/'+file_name)

def test():
	print("test")
