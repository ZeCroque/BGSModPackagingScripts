from enum import StrEnum

class Game(StrEnum):
    STARFIELD = "Starfield"
    FALLOUT4 = "Fallout4"
    SKYRIM = "Skyrim"

def GetAvailableLanguagesSuffixes(gameString):
    match Game(gameString):
        case Game.STARFIELD:
            return ["de", "es", "fr", "it", "ja", "pl", "ptbr", "zhhans"]
        case Game.FALLOUT4:
            return ["de", "es", "esmx", "fr", "it", "ja", "pl", "ptbr", "ru", "cn"]
        case Game.SKYRIM:
            # bsa voicefile suffixes: de, es, fr, it, ja, pl, ru, cn
            return ["german", "spanish", "french", "italian", "japanese", "polish", "russian", "chinese"]
        case _:
            return []

def AskForUserConfirm(question):
    userInput = ""
    while userInput != "y" and userInput != "n":
        print(question + ": y/n")
        userInput = input()

        if userInput != "y" and userInput != "n":
            print("Invalid value")
        print()
    return userInput == "y"