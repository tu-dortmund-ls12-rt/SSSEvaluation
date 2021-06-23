import pathlib
import csv

input_file = [[[
    {'period': 306, 'execution': 7, 'deadline': 306, 'utilization': 0.02552964958565747, 'sslength': 3, 'minSr': 1, 'paths': [{'Cseg': [2, 5], 'Sseg': [3], 'deadline': [-1, -1]}, {'Cseg': [1, 6], 'Sseg': [3], 'deadline': [-1, -1]}], 'Cseg': [2, 6], 'Sseg': [3]}, 
    {'period': 8348, 'execution': 621, 'deadline': 8348, 'utilization': 0.07447035041434254, 'sslength': 89, 'minSr': 1, 'paths': [{'Cseg': [48, 540], 'Sseg': [89], 'deadline': [-1, -1]}, {'Cseg': [121, 500], 'Sseg': [73], 'deadline': [-1, -1]}], 'Cseg': [121, 540], 'Sseg': [89]}], 
    [{'period': 329, 'execution': 11, 'deadline': 329, 'utilization': 0.036835989192778695, 'sslength': 13, 'minSr': 1, 'paths': [{'Cseg': [8, 1], 'Sseg': [13], 'deadline': [-1, -1]}, {'Cseg': [4, 7], 'Sseg': [11], 'deadline': [-1, -1]}], 'Cseg': [8, 7], 'Sseg': [13]}, 
    {'period': 8757, 'execution': 552, 'deadline': 8757, 'utilization': 0.06316401080722131, 'sslength': 308, 'minSr': 1, 'paths': [{'Cseg': [45, 454], 'Sseg': [308], 'deadline': [-1, -1]}, {'Cseg': [234, 318], 'Sseg': [270], 'deadline': [-1, -1]}], 'Cseg': [234, 454], 'Sseg': [308]}]], 
    [[{'period': 165, 'execution': 2, 'deadline': 165, 'utilization': 0.014154219076125352, 'sslength': 2, 'minSr': 1, 'paths': [{'Cseg': [1, 1], 'Sseg': [2], 'deadline': [-1, -1]}, {'Cseg': [1, 1], 'Sseg': [2], 'deadline': [-1, -1]}], 'Cseg': [1, 1], 'Sseg': [2]}, 
    {'period': 7353, 'execution': 998, 'deadline': 7353, 'utilization': 0.13584578092387464, 'sslength': 151, 'minSr': 1, 'paths': [{'Cseg': [125, 704], 'Sseg': [151], 'deadline': [-1, -1]}, {'Cseg': [12, 986], 'Sseg': [132], 'deadline': [-1, -1]}], 'Cseg': [125, 986], 'Sseg': [151]}], 
    [{'period': 201, 'execution': 8, 'deadline': 201, 'utilization': 0.047963404256682454, 'sslength': 17, 'minSr': 1, 'paths': [{'Cseg': [5, 2], 'Sseg': [17], 'deadline': [-1, -1]}, {'Cseg': [4, 4], 'Sseg': [16], 'deadline': [-1, -1]}], 'Cseg': [5, 4], 'Sseg': [17]}, 
    {'period': 6948, 'execution': 708, 'deadline': 6948, 'utilization': 0.10203659574331754, 'sslength': 345, 'minSr': 1, 'paths': [{'Cseg': [278, 430], 'Sseg': [345], 'deadline': [-1, -1]}, {'Cseg': [91, 488], 'Sseg': [331], 'deadline': [-1, -1]}], 'Cseg': [278, 488], 'Sseg': [345]}]]]

with open(str(pathlib.Path(__file__).parent.absolute())+'/'+'example_csv_task_set.csv', 'w') as f:
    w = csv.DictWriter(f, input_file[0][0][0].keys())
    w.writeheader()
    for utilizations in input_file:
            for tasksets in utilizations:
                for task in tasksets:
                    w.writerow(task)
