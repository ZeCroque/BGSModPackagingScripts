import subprocess
import os
import glob
import re
from enum import IntEnum

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

try:
    from . import utils
except ImportError:
    import utils


class CompileMode(IntEnum):
    DEFAULT = 0
    ACHIEVEMENT_FRIENDLY = 1

def GetTemplatedVarValue(name, mode):
    if name == "MOD_VERSION":
        return config.buildCode
    elif name == "MOD_VERSION_STRING":
        return config.modVersionString
    elif name == "IS_AF":
        return "True" if mode == CompileMode.ACHIEVEMENT_FRIENDLY else "False"
    else:
        return "undefined"

def FillTemplates(mode):
    templateFilePaths = glob.glob("./**/*.in", recursive=True)
    for templateFilePath in templateFilePaths:
        with open(templateFilePath, 'r') as file:
            fileData = file.read()
            
        matches = re.findall("\\@(.*)\\@", fileData) 
        for match in matches:
            fileData = fileData.replace("@" + match + "@", GetTemplatedVarValue(match, mode))

        with open(os.path.splitext(templateFilePath)[0], 'w') as file:
            file.write(fileData)

def Compile():
    compiledScriptPaths = glob.glob("./Data/Scripts/**/*.pex", recursive=True)
    for compiledScriptPath in compiledScriptPaths:
        os.remove(compiledScriptPath)
    papyrusCompilerPath = config.gamePath + ("/Tools/Papyrus Compiler/PapyrusCompiler.exe" if config.game == utils.Game.STARFIELD else "/Papyrus Compiler/PapyrusCompiler.exe")
    if(config.game == utils.Game.SKYRIM):
        subprocess.run([papyrusCompilerPath, "Data\\Source\\Scripts", "-i=Data\\Source\\Scripts;" + config.gamePath + "/Data/Source/Scripts", "-o=Data\\Scripts", "-f=TESV_Papyrus_Flags.flg", "-all", "-optimize"])
    else:
        subprocess.run([papyrusCompilerPath, config.modName + "Release.ppj"])

def main():
    mode = -1
    while mode != CompileMode.DEFAULT and mode != CompileMode.ACHIEVEMENT_FRIENDLY:
        print("Enter build mode\n 0: Non-Achievement-Friendly\n 1: Achievement-Friendly")
        try :
            mode = int(input())
        except ValueError :
            print ("Not a number")
        else:
            if mode != CompileMode.DEFAULT and mode != CompileMode.ACHIEVEMENT_FRIENDLY:
                print("Invalid value")
        print()
    FillTemplates(mode)
    Compile()

if __name__ == "__main__":
    main()