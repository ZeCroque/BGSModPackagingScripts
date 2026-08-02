import json

from dataclasses import dataclass

@dataclass
class Config:
    modName: str = ""
    modNameLowerCase: str = ""
    archiveNameBase: str = ""
    mainArchiveName: str = ""
    mainArchiveNameAF: str = ""
    modFilePathAF: str = ""
    archiveExtension: str = ".ba2"
    buildFolder: str = "./build/"
    modVersionString: str = ""
    buildCode: str = ""
    modShortName: str = ""
    game: str = ""
    gamePath: str = ""

    def __post_init__(self):
        with open("preset.json", "r") as file:
            data = json.load(file)
            self.modName = data["modName"]
            self.modNameLowerCase = self.modName.lower()
            self.archiveNameBase = self.modName + " - "
            self.mainArchiveName = self.archiveNameBase + "Main" 
            self.mainArchiveNameAF = self.modName + "_AF - Main"
            self.modFilePathAF = "./Data/" + self.modName + "_AF.esm"
            self.modVersionString = data["modVersion"]
            self.buildCode = data["buildCode"] + ".0"
            self.modShortName = data["modShortName"]
            self.game = data["game"]
            self.gamePath = data["gamePath"]

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

config = Config()

if __name__ == "__main__":
    main()

