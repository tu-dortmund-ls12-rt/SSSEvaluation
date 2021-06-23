import os
import csv
from pathlib import Path

xml_file_content = ['<?xml version="1.0" encoding="utf-8"?>\r\n', "<!DOCTYPE nta PUBLIC '-//Uppaal Team//DTD Flat System 1.1//EN' 'http://www.it.uu.se/research/group/darts/uppaal/flat-1_2.dtd'>\r\n", '<nta>\r\n', '\t<declaration>\n', '\n', 'const int N = 2;\n', 'const int M = 1;\n', 'const int MaxSegmentNumber = 2;\n', '\n', 'typedef int[0, N - 1] id_t;\n', 'typedef struct {\n', '    int period;\n', '    int deadline;\n', '    int offset;\n', '    int pri;\n', '    int number_of_segments;\n', '    struct {\n', '        int s_min;\n', '        int s_max;\n', '        int c_min;\n', '        int c_max;\n', '    } segments[MaxSegmentNumber];\n', '} task_t;\n', '\n', 'id_t queue[N];\n', 'int[0,N] queue_len = 0;\n', 'int[0, M] avail_processors = M;\n', '\n', 'urgent chan run[N];\n', 'broadcast chan synch, first_synch;\n', 'chan priority first_synch &lt; run;\n', 'chan priority synch &lt; run;\n', '\n', 'const task_t Tasks[N] = {{ 4, 4, 0, 1, 2, {{0,  0, 0, 1}, {0, 0, 0, 1}}}, { 20, 20, 4, 2, 1, {{0, 0, 4, 4}, {0, 0, 0, 0}}}};\n', '\n', '</declaration>\r\n', '\t<template>\r\n', '\t\t<name x="40" y="16">Periodic_Task</name>\r\n', '\t\t<parameter>const id_t id</parameter>\r\n', '\t\t<declaration>\n', '\n', 'clock x, t;\n', '\n', 'int[0, MaxSegmentNumber - 1] seg_idx;\n', '\n', 'void enqueue() {\n', '    int tmp;\n', '    queue[queue_len++] = id;\n', '    if (queue_len &gt; 0) {\n', '        int i = queue_len - 1;\n', '        while (i &gt;= 1 &amp;&amp; Tasks[queue[i]].pri &lt; Tasks[queue[i - 1]].pri) {\n', '            tmp = queue[i - 1];\n', '            queue[i - 1] = queue[i];\n', '            queue[i] = tmp;\n', '            i--;\n', '        }\n', '    }\n', '}\n', '\n', 'int period() {\n', '    return Tasks[id].period;\n', '}\n', '\n', 'int deadline() {\n', '    return Tasks[id].deadline;\n', '}\n', '\n', 'int offset() {\n', '    return Tasks[id].offset;\n', '}\n', '\n', 'int pri() {\n', '    return Tasks[id].pri;\n', '}\n', '\n', 'int s_min() {\n', '    return Tasks[id].segments[seg_idx].s_min;\n', '}\n', '\n', 'int s_max() {\n', '    return Tasks[id].segments[seg_idx].s_max;\n', '}\n', '\n', 'int c_min() {\n', '    return Tasks[id].segments[seg_idx].c_min;\n', '}\n', '\n', 'int c_max() {\n', '    return Tasks[id].segments[seg_idx].c_max;\n', '}\n', '\n', 'bool is_last_segment() {\n', '    return seg_idx == Tasks[id].number_of_segments - 1;\n', '}\n', '\n', '</declaration>\r\n', '\t\t<location id="id0" x="807" y="391">\r\n', '\t\t\t<name x="815" y="365">Running</name>\r\n', '\t\t\t<label kind="invariant" x="824" y="391">x &lt;= c_max()</label>\r\n', '\t\t</location>\r\n', '\t\t<location id="id1" x="807" y="85">\r\n', '\t\t\t<name x="815" y="60">Suspended</name>\r\n', '\t\t\t<label kind="invariant" x="824" y="85">x &lt;= s_max()</label>\r\n', '\t\t</location>\r\n', '\t\t<location id="id2" x="450" y="229">\r\n', '\t\t\t<name x="459" y="203">Completed</name>\r\n', '\t\t\t<label kind="invariant" x="467" y="229">t &lt;= period()</label>\r\n', '\t\t</location>\r\n', '\t\t<location id="id3" x="807" y="-59">\r\n', '\t\t\t<name x="815" y="-84">Start</name>\r\n', '\t\t\t<label kind="invariant" x="824" y="-59">t &lt;= offset()</label>\r\n', '\t\t</location>\r\n', '\t\t<location id="id4" x="1020" y="238">\r\n', '\t\t\t<name x="1028" y="212">Miss</name>\r\n', '\t\t</location>\r\n', '\t\t<location id="id5" x="807" y="238">\r\n', '\t\t\t<name x="815" y="213">Ready</name>\r\n', '\t\t</location>\r\n', '\t\t<init ref="id3"/>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id1"/>\r\n', '\t\t\t<target ref="id4"/>\r\n', '\t\t\t<label kind="guard" x="901" y="68">t &gt;  deadline()</label>\r\n', '\t\t\t<nail x="1020" y="85"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id0"/>\r\n', '\t\t\t<target ref="id1"/>\r\n', '\t\t\t<label kind="guard" x="629" y="153">!is_last_segment() &amp;&amp;\n', 'x &gt;= c_min() &amp;&amp;\n', 't &lt;= deadline()</label>\r\n', '\t\t\t<label kind="synchronisation" x="629" y="204">first_synch?</label>\r\n', '\t\t\t<label kind="assignment" x="629" y="221">x = 0,\n', 'seg_idx++,\n', 'avail_processors++</label>\r\n', '\t\t\t<nail x="620" y="374"/>\r\n', '\t\t\t<nail x="620" y="136"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id0"/>\r\n', '\t\t\t<target ref="id2"/>\r\n', '\t\t\t<label kind="guard" x="459" y="280">is_last_segment() &amp;&amp;\n', 'x &gt;= c_min() &amp;&amp;\n', 't &lt;= deadline()</label>\r\n', '\t\t\t<label kind="synchronisation" x="459" y="331">first_synch?</label>\r\n', '\t\t\t<label kind="assignment" x="458" y="348">seg_idx = 0,\n', 'avail_processors++</label>\r\n', '\t\t\t<nail x="450" y="391"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id0"/>\r\n', '\t\t\t<target ref="id0"/>\r\n', '\t\t\t<label kind="guard" x="688" y="306">x &gt;= c_min() &amp;&amp;\n', 'x &lt; c_max() &amp;&amp;\n', 't &lt;= deadline()</label>\r\n', '\t\t\t<label kind="synchronisation" x="688" y="356">first_synch?</label>\r\n', '\t\t\t<nail x="764" y="374"/>\r\n', '\t\t\t<nail x="781" y="348"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id1"/>\r\n', '\t\t\t<target ref="id5"/>\r\n', '\t\t\t<label kind="guard" x="816" y="119">x &gt;= s_min() &amp;&amp;\n', 't &lt;= deadline()</label>\r\n', '\t\t\t<label kind="synchronisation" x="816" y="153">synch?</label>\r\n', '\t\t\t<label kind="assignment" x="816" y="170">enqueue()</label>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id1"/>\r\n', '\t\t\t<target ref="id1"/>\r\n', '\t\t\t<label kind="guard" x="688" y="0">x &gt;= s_min() &amp;&amp;\n', 'x &lt; s_max() &amp;&amp;\n', 't &lt;= deadline()</label>\r\n', '\t\t\t<label kind="synchronisation" x="688" y="51">synch?</label>\r\n', '\t\t\t<nail x="764" y="68"/>\r\n', '\t\t\t<nail x="781" y="43"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id2"/>\r\n', '\t\t\t<target ref="id1"/>\r\n', '\t\t\t<label kind="guard" x="459" y="102">t == period()</label>\r\n', '\t\t\t<label kind="synchronisation" x="459" y="119">synch?</label>\r\n', '\t\t\t<label kind="assignment" x="459" y="136">t = 0,\n', 'x = 0</label>\r\n', '\t\t\t<nail x="450" y="85"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id3"/>\r\n', '\t\t\t<target ref="id1"/>\r\n', '\t\t\t<label kind="guard" x="816" y="-34">t == offset()</label>\r\n', '\t\t\t<label kind="synchronisation" x="816" y="-17">synch?</label>\r\n', '\t\t\t<label kind="assignment" x="816" y="0">t = 0,\n', 'x = 0,\n', 'seg_idx = 0</label>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id5"/>\r\n', '\t\t\t<target ref="id4"/>\r\n', '\t\t\t<label kind="guard" x="901" y="221">t &gt;  deadline()</label>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id0"/>\r\n', '\t\t\t<target ref="id4"/>\r\n', '\t\t\t<label kind="guard" x="909" y="374">t &gt;  deadline()</label>\r\n', '\t\t\t<nail x="1020" y="391"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id5"/>\r\n', '\t\t\t<target ref="id0"/>\r\n', '\t\t\t<label kind="synchronisation" x="816" y="280">run[id]?</label>\r\n', '\t\t\t<label kind="assignment" x="816" y="297">x = 0</label>\r\n', '\t\t</transition>\r\n', '\t</template>\r\n', '\t<template>\r\n', '\t\t<name>Synchronizer</name>\r\n', '\t\t<location id="id6" x="-272" y="-357">\r\n', '\t\t\t<committed/>\r\n', '\t\t</location>\r\n', '\t\t<location id="id7" x="-357" y="-357">\r\n', '\t\t\t<committed/>\r\n', '\t\t</location>\r\n', '\t\t<location id="id8" x="-476" y="-357">\r\n', '\t\t</location>\r\n', '\t\t<init ref="id8"/>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id6"/>\r\n', '\t\t\t<target ref="id8"/>\r\n', '\t\t\t<label kind="synchronisation" x="-459" y="-416">synch!</label>\r\n', '\t\t\t<nail x="-272" y="-416"/>\r\n', '\t\t\t<nail x="-476" y="-416"/>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id7"/>\r\n', '\t\t\t<target ref="id6"/>\r\n', '\t\t\t<label kind="synchronisation" x="-340" y="-374">synch!</label>\r\n', '\t\t</transition>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id8"/>\r\n', '\t\t\t<target ref="id7"/>\r\n', '\t\t\t<label kind="synchronisation" x="-459" y="-374">first_synch!</label>\r\n', '\t\t</transition>\r\n', '\t</template>\r\n', '\t<template>\r\n', '\t\t<name x="40" y="16">Scheduler</name>\r\n', '\t\t<declaration>\n', '\n', 'void dequeue() {\n', '    int i = 0;\n', '    queue_len -= 1;\n', '    while (i &lt; queue_len)\n', '    {\n', '        queue[i] = queue[i + 1];\n', '        i++;\n', '    }\n', '    queue[i] = 0;\n', '}\n', '\n', 'id_t front() {\n', '    return queue[0];\n', '}\n', '\n', 'bool job_ready() {\n', '    return queue_len &gt; 0;\n', '}\n', '\n', 'bool processor_avail() {\n', '    return avail_processors &gt; 0;\n', '}\n', '\n', '</declaration>\r\n', '\t\t<location id="id9" x="153" y="161">\r\n', '\t\t\t<name x="161" y="136">Scheduling</name>\r\n', '\t\t</location>\r\n', '\t\t<init ref="id9"/>\r\n', '\t\t<transition>\r\n', '\t\t\t<source ref="id9"/>\r\n', '\t\t\t<target ref="id9"/>\r\n', '\t\t\t<label kind="guard" x="-17" y="68">job_ready() &amp;&amp;\n', 'processor_avail()</label>\r\n', '\t\t\t<label kind="synchronisation" x="-17" y="102">run[front()]!</label>\r\n', '\t\t\t<label kind="assignment" x="-17" y="119">dequeue(),\n', 'avail_processors--</label>\r\n', '\t\t\t<nail x="111" y="144"/>\r\n', '\t\t\t<nail x="128" y="119"/>\r\n', '\t\t</transition>\r\n', '\t</template>\r\n', '\t<system>\n', '\n', 'system Scheduler, Synchronizer, Periodic_Task;\n', '\n', '</system>\r\n', '\t<queries>\r\n', '\t</queries>\r\n', '</nta>\r\n']
q_file_content = "A[] forall (i : id_t) not Periodic_Task(i).Miss"

def Uppaal(tasks,i):
    len_tasks = len(tasks)
    utilization = sum([task['utilization'] for task in tasks])

    Path(os.getcwd()+"/schedTest/inputs").mkdir(parents=True, exist_ok=True)
    Path(os.getcwd()+"/schedTest/temp_models").mkdir(parents=True, exist_ok=True)

    file_name = os.getcwd()+'/schedTest/inputs/uppaal_N='+str(len_tasks)+'_M='+str(len(tasks[0]['Cseg']))+"_U="+str(utilization)+"_"+str(i)+'.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        for i in range(len_tasks):
            writer.writerow(['T', i+1, tasks[i]['period'], tasks[i]['deadline']])
            writer.writerow(['V', i+1, len(tasks[i]['Cseg']), 0, tasks[i]['sslength'], 0, tasks[i]['execution']])
    
    schedulability_result = uppaal_schedulability(file_name)
    os.system("rm " + file_name)
    

    return schedulability_result

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
   return (a * b) // gcd(a,b)

def uppaal_schedulability(input_file_name):
    global xml_file_content, q_file_content
    N = int(input_file_name.split("N=")[1].split("_")[0])
    M = int(input_file_name.split("M=")[1].split("_")[0])
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