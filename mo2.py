import os
import re
import subprocess

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

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
    subprocess.run([config.mo2Path + "/ModOrganizer.exe", "-p", "ZZZ_" + config.modName, "moshortcut://" + config.mo2InstanceName + ":" + target])

def runMO2TargetWithArgs(target, exe, args):
    replaceMO2LaunchArgs(exe, args)
    runMO2Target(target)
    replaceMO2LaunchArgs(exe, "")
    
def runCK():
    runMO2Target("Creation Kit")

def runCKWithArgs(args):
    runMO2TargetWithArgs("Creation Kit", "CreationKit.exe", args) 