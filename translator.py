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

def CreateAllStringFiles():
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

    mo2.RunCKWithArgs("-TagifyPlugin:" + config.modName + ".esp")
    mo2.RunCKWithArgs("-ExportText:" + config.modName + ".esp")
    mo2.RunCKWithArgs("-CompileTextExport:" + config.modName + ".esp " + utils.GetEnglishSuffix(utils.Game(config.game)) + " \\\"" + textExportPath + "\\\"")
    CreateAllStringFiles()
    if config.game == utils.Game.STARFIELD:
        if config.modSize != utils.ModSize.FULL:
            mo2.RunCK() #User needs to manually convert to .esm here
        mo2.RunCKWithArgs("-DelocalizeMasterfile:"+ config.modName + ".esm")
    else:
        if config.modSize == utils.ModSize.SMALL:
            mo2.RunCKWithArgs("-ConvertToESL:"+ config.modName + ".esp")
            mo2.RunCKWithArgs("-DelocalizeLocalMasterfile:"+ config.modName + ".esl")
            os.remove("./Data/" + config.modName + "_TempCopy.esl")
        else:
            mo2.RunCKWithArgs("-DelocalizeLocalMasterfile:"+ config.modName + ".esp")
            os.remove("./Data/" + config.modName + "_TempCopy.esp")

def main():
    Translate()

if __name__ == "__main__":
    main()