"""
Schedulability test from the paper: Response-Time Analysis for Self-Suspending Tasks
Under EDF Scheduling. Federico Aromolo, Alessandro Biondi, Geoffrey Nelissen
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECRTS.2022.13
"""

import os
import csv
from pathlib import Path

"""
-------------------------------------------------
 Framework >>>   (rta)
 execution       wcet
 sslenght        suspension
 period          period
 deadline        deadline
                 wcrt_ub=0
"""
BINARY = Path(__file__).parent / "edf_rta_sched"

def RTA(tasks):

   #Write the tasks to csv file to be parsed in th rta project.
   csv_file_name = write_task_to_csv_file(tasks)

   result = rta_schedulability(csv_file_name)

   os.system(f"rm '{csv_file_name}'")

   return result

def write_task_to_csv_file(tasks):
    """
    create csv file in this fromat:
    wcet | suspension | period | deadline
    value| value     | value   | value
    value| value     | value   | value
    """

    #if there is no directory for inputs, crate one
    inputs_dir = Path(os.getcwd()) /"schedTest" / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    file_name = inputs_dir / f"edf_rta_N={len(tasks)}.csv"
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['wcet', 'suspension', 'period', 'deadline'])

        for task in tasks:
            wcet = task['execution']
            suspension = task['sslength']
            period = task['period']
            deadline = task['deadline']
            writer.writerow([wcet, suspension, period, deadline])

    return file_name

def rta_schedulability(file_name):
    """
    run the compiled c++ file with csv file as argument.
    """

    raw = os.popen(f"{BINARY} {file_name}").read()
    output = raw.strip()
    #print(output)
    if output == 'false':
        return False
    else:
        return True
def print_tasks(tasks):
    for task in tasks:
        print(f"""
        ------------------------------
        wcet       : {task['execution']}
        suspension : {task['sslength']}
        period     : {task['period']}
        deadline   : {task['deadline']}
        ------------------------------
        """)

