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
    mo2IniPath = os.getenv('LOCALAPPDATA') + "\\ModOrganizer\\" + config.game + "\\ModOrganizer.ini"
    with open(mo2IniPath, 'r') as file:
        fileData = file.read()

    matches = re.findall("(.)\\\\.*CreationKit.exe", fileData) 
    index = matches[0]

    matches = re.findall("(" + index + "\\\\arguments=)(.*)", fileData) 
    fileData = fileData.replace(matches[0][0] + matches[0][1], matches[0][0] + args)

    with open(mo2IniPath, 'w') as file:
        file.write(fileData)

def runCK():
    subprocess.run(["J:/100Install/mo2/ModOrganizer.exe", "-p", "ZZZ_" + config.modName, "moshortcut://" + config.game + ":Creation Kit"])

def createAllStringFiles():
    stringFiles = os.listdir("./Data/Strings")
    supportedLanguages = utils.GetAvailableLanguagesSuffixes(utils.Game(config.game))

    for supportedLanguage in supportedLanguages:
        for stringFile in stringFiles:
            shutil.copy("./Data/Strings/" + stringFile, "./Data/Strings/" + stringFile.replace("en", supportedLanguage))

def Translate():
    if os.path.isdir("./Data/Strings/"):
        shutil.rmtree("./Data/Strings/")

    textExportPath = config.gamePath + "TextExport/" + config.modName + ".esp"
    if os.path.isdir(textExportPath):
        shutil.rmtree(textExportPath)

    replaceCKLaunchArgs("-TagifyPlugin:" + config.modName + ".esp")
    runCK()
    replaceCKLaunchArgs("-ExportText:" + config.modName + ".esp")
    runCK()
    replaceCKLaunchArgs("-CompileTextExport:" + config.modName + ".esp en " + textExportPath)
    runCK()
    createAllStringFiles()
    replaceCKLaunchArgs("")
    runCK()
    replaceCKLaunchArgs("-DelocalizeMasterfile:"+ config.modName + ".esm")
    runCK()
    replaceCKLaunchArgs("")

def main():
    Translate()

if __name__ == "__main__":
    main()