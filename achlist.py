import re

try:
    from . import utils
except ImportError:
    import utils

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

def AppendStringfilesToAchlist():
    achlist = "./Data/" + config.modShortName + "_Main.achlist"
    with open(achlist, "r") as input:
        inputString = input.read()

        stringList = '",\n'
        supportedLanguages = utils.GetAvailableLanguagesSuffixes(config.game)
        for supportedLanguage in supportedLanguages:
            prefix = r'    "Data\\\\Strings\\\\' + config.modName + "_" + supportedLanguage
            stringList += prefix + r'.STRINGS",' + "\n"
            stringList += prefix + r'.DLSTRINGS",' + "\n"
            stringList += prefix + r'.ILSTRINGS"'
            if supportedLanguage != supportedLanguages[-1]:
                stringList += ",\n"
            else:
                stringList += "\n]"
        inputString = re.sub(r'"\n\]', stringList, inputString)
        with open(achlist, "w") as output:
            output.write(inputString)

def main():
    AppendStringfilesToAchlist()

if __name__ == "__main__":
    main()