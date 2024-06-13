import os
import csv
from pathlib import Path

with open(os.getcwd()+'/schedTest/uppaal_periodic.xml', 'r') as xml_file:
	xml_file_content = xml_file.read().splitlines()
q_file_content = "A[] forall (i : id_t) not Periodic_Task(i).Miss"

# NOTE: this UPPAAL test is for non-preemptive PERIODIC tasks on MULTICORE.
#		Since the generic framework does not support multicore, we set 
#		the number of cores to 1 by default. 
# NOTE 2: There exists a version of the test for SPORADIC tasks too 
#		  that was not integrated in the generic framework. Check
#		  https://github.com/beyazit-yalcinkaya/date2019 for details.
def UPPAAL(tasks, i, n_cores=1):
	len_tasks = len(tasks)
	utilization = sum([task['utilization'] for task in tasks])

	Path(os.getcwd()+"/schedTest/inputs").mkdir(parents=True, exist_ok=True)
	Path(os.getcwd()+"/schedTest/temp_models").mkdir(parents=True, exist_ok=True)

	file_name = os.getcwd()+'/schedTest/inputs/uppaal_N='+str(len_tasks)+'_M='+str(n_cores)+"_U="+str(utilization)+"_"+str(i)+'.csv'
	with open(file_name, 'w', newline='') as file:
		writer = csv.writer(file)
		for i in range(len_tasks):
			writer.writerow(['T', i+1, tasks[i]['period'], tasks[i]['deadline']])
			n_segments = len(tasks[i]['Cseg'])

			for j in range(n_segments):
				if j == 0:
					writer.writerow(['V', i+1, 1, 0, tasks[i].get('jitter', 0), tasks[i].get('Cseg_min', [0]*n_segments)[j], tasks[i]['Cseg'][j]])
				else:
					writer.writerow(['V', i+1, j+1, tasks[i].get('Sseg_min', [0]*n_segments)[j-1], tasks[i]['Sseg'][j-1], tasks[i].get('Cseg_min', [0]*n_segments)[j], tasks[i]['Cseg'][j]])
	
	schedulability_result = uppaal_schedulability(file_name, len_tasks, n_cores)
	os.system("rm " + file_name)
	

	return schedulability_result

def gcd(a, b):
	while b:
		a, b = b, a % b
	return a

def lcm(a, b):
	return (a * b) // gcd(a,b)

def uppaal_schedulability(input_file_name, n_tasks, n_cores):
	global xml_file_content, q_file_content
	N = n_tasks
	M = n_cores
	input_file = open(input_file_name, "r")
	input_file_content = [line[:-1].split(",") for line in input_file.readlines()]#list(map(lambda x: x[:-1].split(", "), input_file.readlines()))
	input_file.close()
	tasks = "const task_t Tasks[N] = {"
	hyperperiod = 1
	periods = []
	offset = 0
	l = len(input_file_content)
	max_number_of_segments = max(map(lambda x: int(x[2]), filter(lambda x: x[0] == "V", input_file_content)))
	for i in range(l):
		if input_file_content[i][0] == 'T':
			if i != 0:
				tasks += str(number_of_segments) + ", {" + ", ".join(segments + ["{0, 0, 0, 0}"] * (max_number_of_segments - number_of_segments)) + "}}, "
			segments = []
			number_of_segments = 0
			priority = int(input_file_content[i][1])
			period = int(float(input_file_content[i][2]))
			deadline = int(float(input_file_content[i][3]))
			periods.append(period)
			hyperperiod = lcm(hyperperiod, period)
			tasks += "{" + str(period) + ", " + str(deadline) + ", " + str(offset) + ", " + str(priority) + ", "
			if i == 0:
				min_period = str(period)
		elif input_file_content[i][0] == 'V':  
			segments.append("{" + str(int(float(input_file_content[i][3]))) + ", " + str(int(float(input_file_content[i][4]))) + ", " + str(int(float(input_file_content[i][5]))) + ", " + str(int(float(input_file_content[i][6]))) + "}")
			number_of_segments += 1
			if i == l - 1:
				max_period = str(period)
	number_of_jobs = sum(map(lambda x: hyperperiod / x, periods))
	tasks += str(number_of_segments) + ", {" + ", ".join(segments + ["{0, 0, 0, 0}"] * (max_number_of_segments - number_of_segments)) + "}}};"
	xml_file_content[5] = "const int N = " + str(N) + ";\n"
	xml_file_content[6] = "const int M = " + str(M) + ";\n"
	xml_file_content[7] = "const int MaxSegmentNumber = " + str(max_number_of_segments) + ";\n"
	xml_file_content[33] =  tasks + "\n"
	xml_file_name = os.getcwd() + "/schedTest/temp_models/" + input_file_name.split("inputs/")[1].split(".csv")[0] + ".xml"
	xml_file = open(xml_file_name, "w+")
	xml_file.writelines(xml_file_content)
	xml_file.close()
	q_file_name = os.getcwd() + "/schedTest/temp_models/" + input_file_name.split("inputs/")[1].split(".csv")[0] + ".q"
	q_file = open(q_file_name, "w+")
	q_file.write(q_file_content)
	q_file.close()
	result = verify_xml_file(N, xml_file_name, q_file_name, min_period, max_period, str(number_of_jobs), input_file_name, "1h")

	if result != 'Timedout':
		if result == "1":
			return True
	return False



"""
	A general function that can be applied to any framework using UPPAAL.
	All parameters of the function must be provided by the user.
	Output format:
		File Name, Result, Number of jobs in hyperperiod, Explored states, Time (seconds), Virtual memory (KB), Resident memory (KB), Minimum period, Maximum period
"""

def verify_xml_file(N, xml_file_name , q_file_name, min_period, max_period, number_of_jobs, csv_file_name, timeout_value):
	output = os.popen("timeout " + timeout_value + " ./schedTest/verifyta -C -S1 -b -u " + xml_file_name + " " + q_file_name).read()
	if "Formula is satisfied." in output:
		Result = "1"
	elif "Formula MAY be satisfied." in output:
		Result = "May be schedulable"
	elif "Formula MAY NOT be satisfied." in output:
		Result = "May not be schedulable"
	elif "Formula is NOT satisfied." in output:
		Result = "0"
	else:
		Result = "Timedout"
	# if Result == "Timedout":
	#     output_line = csv_file_name + ", " + Result + ", " + number_of_jobs + ", -, -, -, -, " + min_period + ", " + max_period
	# else:
	#     output = output.split("\n")
	#     time = str(float(output[11].split(" ")[-2]) * 0.001)
	#     states_explored = output[10].split(" ")[-2]
	#     virtual_memory = output[12].split(" ")[-2]
	#     resident_memory = output[13].split(" ")[-2]
	#     output_line = csv_file_name + ", " + Result + ", " + number_of_jobs + ", " + states_explored + ", " + time + ", " + virtual_memory + ", " + resident_memory + ", " + min_period + ", " + max_period
	#print(output_line)
	os.system("rm " + xml_file_name)
	os.system("rm " + q_file_name)
	return Result