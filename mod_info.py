import json

from dataclasses import dataclass

try:
    from . import utils
except ImportError:
    import utils

@dataclass
class Config:
    modName: str = ""
    modNameLowerCase: str = ""
    archiveNameBase: str = ""
    mainArchiveName: str = ""
    mainArchiveNameAF: str = ""
    modFilePathAF: str = ""
    archiveExtension: str = ""
    buildFolder: str = "./build/"
    modVersionString: str = ""
    buildCode: str = ""
    modShortName: str = ""
    game: str = ""
    gamePath: str = ""
    mo2Path: str = ""
    mo2InstanceName: str = ""
    pluginExtension: str = ""

    def __post_init__(self):
        with open("preset.json", "r") as file:
            data = json.load(file)
            self.modName = data["modName"]
            self.modNameLowerCase = self.modName.lower()
            self.modVersionString = data["modVersion"]
            self.buildCode = data["buildCode"] + ".0"
            self.modShortName = data["modShortName"]
            self.game = data["game"]
            self.gamePath = data["gamePath"]
            self.mo2Path = data["mo2Path"]
            self.mo2InstanceName = data["mo2InstanceName"]              
            self.archiveExtension = ".bsa" if utils.Game(self.game) == utils.Game.SKYRIM else ".ba2"            
            self.pluginExtension = (".esm" if utils.Game(self.game) == utils.Game.STARFIELD else ".esp")
            self.archiveNameBase = self.modName + " - "          
            self.mainArchiveName = self.archiveNameBase + "Main" if utils.Game(self.game) != utils.Game.SKYRIM else self.modName
            self.mainArchiveNameAF = self.modName + "_AF - Main" if utils.Game(self.game) != utils.Game.SKYRIM else self.modName + "_AF"
            self.modFilePathAF = "./Data/" + self.modName + "_AF" + self.pluginExtension

def main():   
    print("modName: " + config.modName)
    print("modNameLowerCase: " + config.modNameLowerCase)
    print("archiveNameBase: " + config.archiveNameBase)
    print("mainArchiveName: " + config.mainArchiveName)
    print("mainArchiveNameAF: " + config.mainArchiveNameAF)
    print("modFilePathAF: " + config.modFilePathAF)
    print("archiveExtension: " + config.archiveExtension)
    print("buildFolder: " + config.buildFolder)
    print("modVersionString: " + config.modVersionString)
    print("buildCode: " + config.buildCode)
    print("modShortName: " + config.modShortName)
    print("game: " + config.game)
    print("gamePath: " + config.gamePath)
    print("mo2Path: " + config.mo2Path)
    print("mo2InstanceName: " + config.mo2InstanceName)
    print("pluginExtension: " + config.pluginExtension)

config = Config()

if __name__ == "__main__":
    main()

