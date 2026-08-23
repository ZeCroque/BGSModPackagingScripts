import subprocess
import os
import re
import shutil

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

try:
    from . import utils
except ImportError:
    import utils

def replaceCKLaunchArgs(args):
    mo2IniPath = os.getenv('LOCALAPPDATA') + "\\ModOrganizer\\" + config.mo2InstanceName + "\\ModOrganizer.ini"
    with open(mo2IniPath, 'r') as file:
        fileData = file.read()

    matches = re.findall("(.)\\\\.*CreationKit.exe", fileData) 
    index = matches[0]

    matches = re.findall("(" + index + "\\\\arguments=)(.*)", fileData) 
    fileData = fileData.replace(matches[0][0] + matches[0][1], matches[0][0] + args)

    with open(mo2IniPath, 'w') as file:
        file.write(fileData)

def runCK():
    subprocess.run([config.mo2Path + "/ModOrganizer.exe", "-p", "ZZZ_" + config.modName, "moshortcut://" + config.mo2InstanceName + ":Creation Kit"])

def createAllStringFiles():
    stringFiles = os.listdir("./Data/Strings")
    supportedLanguages = utils.GetAvailableLanguagesSuffixes(utils.Game(config.game))

    enSuffix = utils.GetEnglishSuffix(utils.Game(config.game))
    for supportedLanguage in supportedLanguages:
        for stringFile in stringFiles:
            shutil.copy("./Data/Strings/" + stringFile, "./Data/Strings/" + stringFile.replace(enSuffix, supportedLanguage))

def Translate():
    if os.path.isdir("./Data/Strings/"):
        shutil.rmtree("./Data/Strings/")

    textExportPath = config.gamePath + "/TextExport/" + config.modName + ".esp"
    if os.path.isdir(textExportPath):
        shutil.rmtree(textExportPath)

    replaceCKLaunchArgs("-TagifyPlugin:" + config.modName + ".esp")
    runCK()
    replaceCKLaunchArgs("-ExportText:" + config.modName + ".esp")
    runCK()
    replaceCKLaunchArgs("-CompileTextExport:" + config.modName + ".esp " + utils.GetEnglishSuffix(utils.Game(config.game)) + " \\\"" + textExportPath + "\\\"")
    runCK()
    createAllStringFiles()
    replaceCKLaunchArgs("")
    runCK()
    if config.game == utils.Game.STARFIELD:
        replaceCKLaunchArgs("-DelocalizeMasterfile:"+ config.modName + ".esp")
        runCK()
    else:
        replaceCKLaunchArgs("-DelocalizeLocalMasterfile:"+ config.modName + ".esp")
        runCK()
        os.remove("./Data/" + config.modName + "_TempCopy.esp")
    replaceCKLaunchArgs("")

def main():
    Translate()

if __name__ == "__main__":
    main()