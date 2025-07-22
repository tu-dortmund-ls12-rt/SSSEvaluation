"""
Schedulability test from the paper: Response-Time Analysis for Self-Suspending Tasks
Under EDF Scheduling. Federico Aromolo, Alessandro Biondi, Geoffrey Nelissen
https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ECRTS.2022.13

The files will be downloaded and compiled.
"""

"""
-------------------------------------------------
 Framework >>>   (rta)
 execution       wcet
 sslenght        suspension
 period          period
 deadline        deadline
                 wcrt_ub=0
"""

import shutil
import sys
import os
import csv
from pathlib import Path
import subprocess
import platform
import requests
import zipfile
from io import BytesIO

# Path of c++ files.
CPP_DIR = Path(__file__).parent.resolve()

EXE_NAME = "edf_sched_test"
BINARY = CPP_DIR / EXE_NAME

# only those files are needed for this analysis in the framework
SOURCE_FILES = [
    "models.cpp",
    "rta.cpp",
    "dss_rta.cpp",
    "edf_sched_test.cpp",
]

def RTA(tasks):

   download_zip_file()

   compile_if_needed()
   #Write the tasks to csv file to be parsed in th rta project.
   csv_file_name = write_task_to_csv_file(tasks)

   result = rta_schedulability(csv_file_name)

   os.system(f"rm '{csv_file_name}'")

   return result

def download_zip_file():
    """
    Download the zip file and unzip it

    NOTE: If `url` fails (404 or network error) for any reason, go to
    and search under “Supplementary Material” for
    correct link
    """
    RTA_URL = "https://drops.dagstuhl.de/storage/artifacts/darts-vol008/darts-vol008-issue001_ecrts2022/16554/DARTS-8-1-5-artifact-84adbd6adb19a7638bc7fe9dd523735f.zip"

    if all((CPP_DIR / fname).exists() for fname in SOURCE_FILES):
        #all needed files are available.
        return
    try:
        r = requests.get(RTA_URL)
        r.raise_for_status()

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error downloading '{RTA_URL}'") from e

    with zipfile.ZipFile(BytesIO(r.content)) as zip_file:
        zip_file.extractall(CPP_DIR)# or wherever you want

    rta_files = ["models.cpp", "models.h",
    "rta.cpp", "rta.h",
    "dss_rta.cpp", "dss_rta.h"]

    folder = [f for f in CPP_DIR.iterdir() if f.is_dir()]
    unziped_folder  = folder[1] #it expected to be "artifact"
    #copy the rta_files to the folder edf_rta to be available to the compiling process
    for rta_file in rta_files:
        shutil.move(CPP_DIR/unziped_folder/rta_file, CPP_DIR)

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

def compile_if_needed():
    """
    Compile edf_sched_test if it is not already present.
    """
    compiler = find_compiler()
    if compiler is None:
        sys.exit("No C++ compiler found. Install Install C++ Compiler and start the framework again.")

    # choose flags per‐compiler
    if compiler.lower().endswith("cl.exe"):
        flags = ["/EHsc", "/O2"]
        out_flag = ["/Fe" + EXE_NAME + ".exe"]
    else:#for other compilers
        flags = ["-std=c++11", "-O2"]
        out_flag = ["-o", EXE_NAME]

    exe_path = CPP_DIR / EXE_NAME
    if platform.system() == "Windows":
        exe_path = exe_path.with_suffix(".exe")

    if exe_path.exists() and os.access(str(exe_path), os.X_OK):
        #print("edf_sched_test is already compiled")
        return
        #return exe_path

    #print(f"build {EXE_NAME} not found – compiling starts..")
    old_cwd = os.getcwd()
    os.chdir(CPP_DIR)
    try:
        cmd = [compiler, *flags, *out_flag, *SOURCE_FILES]
        #print("build Command:", " ".join(cmd))
        subprocess.check_call(cmd)
        if platform.system() != "Windows":
            exe_path.chmod(0o755)
    finally:
        os.chdir(old_cwd)

    if not exe_path.exists():
        raise RuntimeError("Compilation failed: executable not created.")
    return exe_path


def find_compiler():
    """
    determine if the user have compiler or not and which.
    """
    WINDOWS_COMPILERS = ["g++.exe", "clang.exe", "cl.exe", "icl.exe"]
    operating_system_and_compiler = {
        "Windows": WINDOWS_COMPILERS,
        "Linux":  ["g++", "clang++"],
        "Darwin": ["g++", "clang++"],
    }.get(platform.system(), [])
    for compiler in operating_system_and_compiler:
        if shutil.which(compiler):
            return compiler
    #when the user doesn´t have compiler
    return None

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


if __name__ == "__main__":
    #download_zip_file()
    print("main")
    system = platform.system()
    cmd = shutil.which("clang++")
    print(cmd)
