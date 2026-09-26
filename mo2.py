import os
import re
import subprocess
import psutil
from pathlib import Path

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

try:
    from . import utils
except ImportError:
    import utils

def replaceMO2LaunchArgs(exe, args):
    mo2IniPath = os.getenv('LOCALAPPDATA') + "\\ModOrganizer\\" + config.mo2InstanceName + "\\ModOrganizer.ini"
    with open(mo2IniPath, 'r') as file:
        fileData = file.read()

    matches = re.findall("(.)\\\\.*" + exe, fileData) 
    index = matches[0]

    matches = re.findall("(" + index + "\\\\arguments=)(.*)", fileData) 
    fileData = fileData.replace(matches[0][0] + matches[0][1], matches[0][0] + args)

    with open(mo2IniPath, 'w') as file:
        file.write(fileData)

def runMO2Target(target):
    mo2Exec = Path(config.mo2Path + "/ModOrganizer.exe")

    # Checks if already running and closes accordingly
    for proc in psutil.process_iter(["pid", "exe"]):
        try:            
            exe = proc.info["exe"]

            if exe and Path(exe).resolve() == mo2Exec:
                print()

                if utils.AskForUserConfirm(f"MO2 is already running (PID {proc.pid}). Close it and continue?"):
                    proc.terminate()
        
                    try:
                        proc.wait(timeout=5)
                    except psutil.TimeoutExpired:
                        print("It did not close normally; forcing termination.")
                        proc.kill()
                        proc.wait()
                else:
                    print("Aborted.")
                    raise SystemExit(1)
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
            pass

    subprocess.run([mo2Exec, "-p", "ZZZ_" + config.modName, "moshortcut://" + config.mo2InstanceName + ":" + target])

def runMO2TargetWithArgs(target, exe, args):
    replaceMO2LaunchArgs(exe, args)
    runMO2Target(target)
    replaceMO2LaunchArgs(exe, "")
    
def runCK():
    runMO2Target("Creation Kit")

def runCKWithArgs(args):
    runMO2TargetWithArgs("Creation Kit", "CreationKit.exe", args) 

def main():   
    runMO2Target("xTranslator")

if __name__ == "__main__":
    main()