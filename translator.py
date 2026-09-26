import os
import shutil

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

try:
    from . import utils
except ImportError:
    import utils

try:
    from . import mo2
except ImportError:
    import mo2

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

    mo2.runCKWithArgs("-TagifyPlugin:" + config.modName + ".esp")
    mo2.runCKWithArgs("-ExportText:" + config.modName + ".esp")
    mo2.runCKWithArgs("-CompileTextExport:" + config.modName + ".esp " + utils.GetEnglishSuffix(utils.Game(config.game)) + " \\\"" + textExportPath + "\\\"")
    createAllStringFiles()
    mo2.runCK() #User needs to manually convert to .esm here
    if config.game == utils.Game.STARFIELD:
        mo2.runCKWithArgs("-DelocalizeMasterfile:"+ config.modName + ".esm")
    else:
        mo2.runCKWithArgs("-DelocalizeLocalMasterfile:"+ config.modName + ".esp")
        os.remove("./Data/" + config.modName + "_TempCopy.esp")

def main():
    Translate()

if __name__ == "__main__":
    main()