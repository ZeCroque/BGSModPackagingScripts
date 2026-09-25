import re
import json
import os

try:
    from . import utils
except ImportError:
    import utils

def FormatNexusModPage(outputFolder):
    with open("./readme.md", "r") as input:
        inputString = input.read()

        # Removes index
        outputString = re.sub(r"## Index.*?##", r"##", inputString, flags=re.MULTILINE | re.DOTALL)

        # Formats titles
        outputString = re.sub(r"^# (.*)", r"[size=6]\1[/size]", outputString, flags=re.MULTILINE)
        outputString = re.sub(r"^## ([0-9]*\. )(.*)", lambda m: "[size=5]" + m.group(1) + m.group(2).capitalize() + "[/size]", outputString, flags=re.MULTILINE)
        outputString = re.sub(r"^### (.*)", r"[size=4]\1[/size]", outputString, flags=re.MULTILINE)
        outputString = re.sub(r"^#### (.*)", r"    [b][u]\1[/u][/b]", outputString, flags=re.MULTILINE)

        # Formats title references
        outputString = re.sub(r"`([0-9]*\. )(.*?)`", lambda m: "[i]" + m.group(1) + m.group(2).capitalize() + "[/i]", outputString, flags=re.MULTILINE)    

        # Formats bold and italic
        outputString = re.sub(r"([^\*])\*([^\*]*[^\*])\*", r"\1[i]\2[/i]", outputString, flags=re.MULTILINE)
        outputString = re.sub(r"\*\*(.*)\*\*", r"[b]\1[/b]", outputString, flags=re.MULTILINE)

        # Handles URLs
        outputString = re.sub(r"\[([^]]*?)\]\((.*?)\)", r"[url=\2]\1[/url]", outputString, flags=re.MULTILINE)

        # Handles platform specific tags
        outputString = re.sub(r"@(.*?)@", r"\1", outputString, flags=re.MULTILINE | re.DOTALL)
        outputString = re.sub(r"\|.*?\|", r"", outputString, flags=re.MULTILINE | re.DOTALL)

        # Outputs
        with open(outputFolder + "nexus.txt", "w") as output:
            output.write(outputString)

def FormatReadmeFile(outputFolder):
    with open("./readme.md", "r") as input:
        inputString = input.read()

        # Handles platform specific tags
        outputString = re.sub(r"@(.*?)@", r"\1", inputString, flags=re.MULTILINE | re.DOTALL)
        outputString = re.sub(r"\|.*?\|", r"", outputString, flags=re.MULTILINE | re.DOTALL)

        # Outputs
        with open(outputFolder + "readme.md", "w") as output:
            output.write(outputString)

capturedSections = {}
def EraseAndCapture(m):
    capturedSections[m.group(2)] = m.group(1)
    return m.group(3)

def ExtractSections(inputString):
    # Removes all before first section
    outputString = re.sub(r"#.*?## Index.*?##", r"##", inputString, flags=re.MULTILINE | re.DOTALL)

    # Extracts sections
    while True:
        outputString, count = re.subn(r"(## [0-9]+?\. (.*?)\r?\n.*?)(^## [0-9])+?", EraseAndCapture, outputString, count=1, flags=re.MULTILINE | re.DOTALL)
        if not count:
            break
    capturedSections["FEEDBACK"] = outputString

def PickSections(titles):
    outputString = ""
    i = 1
    for title in titles:
        if title in capturedSections:
            outputString += re.sub(r"^## [0-9]+?\. (.*)", "## " + str(i) + r". \1" if len(titles) > 1 else "", capturedSections[title])
            i += 1
    return outputString

def FormatCreationsModPage(outputFolder):
    with open("./readme.md", "r") as input:
        inputString = input.read()
        sectionsToKeep = ["OVERVIEW", "DETAILS"]
        try:
            with open("./creationsModpageSections.json", "r") as file:
                titles = json.load(file)
                for title in titles:
                    sectionsToKeep.append(title)
        except FileNotFoundError: 
            utils.AskForUserConfirm("The creationsModpageSections.json file is missing, only OVERVIEW and DETAILS will be kept. Continue?")

        ExtractSections(inputString)

        outputString = PickSections(sectionsToKeep)

        # Formats titles
        outputString = re.sub(r"^##", "#", outputString, flags=re.MULTILINE)

        # Handles URLs
        outputString = re.sub(r"\[([^]]*?)\]\(.*?\)", r"\1", outputString, flags=re.MULTILINE)

        # Handles platform specific tags
        outputString = re.sub(r"@.*?@", r"", outputString, flags=re.MULTILINE | re.DOTALL)
        outputString = re.sub(r"\|(.*?)\|", r"\1", outputString, flags=re.MULTILINE | re.DOTALL)

        # Adds creations footer
        outputString += "# " + str(len(sectionsToKeep) + 1) + """. FEEDBACK & MORE

Found a bug or have an idea for new features? Needs more info? Go to my Discord server!
Discord: https://discord.gg/K9Jk4y2tjJ

Want to know more about me and my other projects? Check my links!
LinkTree: https://linktr.ee/zecroque"""

        #Output
        with open(outputFolder + "creations.txt", "w") as output:
            output.write(outputString)

def FormatDiscordTopics(outputFolder):
    with open("./readme.md", "r") as input:
        inputString = input.read()

        ExtractSections(inputString)

        separator = "\n======================================================================================================\n"

        outputString = separator + "Mod Details" + separator + PickSections(["OVERVIEW", "DETAILS"])
        outputString += separator + "Frequently Asked Questions" + separator + PickSections(["FREQUENTLY ASKED QUESTIONS"])
        outputString += separator + "Known Issues" + separator + PickSections(["KNOWN ISSUES"])
        outputString += separator + "Compatibility" + separator + PickSections(["COMPATIBILITY"])
        outputString += separator + "Recommended Mods" + separator + PickSections(["RECOMMENDED MODS"])
        outputString += separator + "Credits" + separator + PickSections(["CREDITS", "TOOLS USED"])
        outputString += separator + "Licensing/Legal" + separator + PickSections(["LICENSING/LEGAL"])

        plannedFeatures = PickSections(["FEEDBACK"])
        plannedFeatures = re.sub(r".*\*\*Planned features:\*\*", r"", plannedFeatures, flags=re.MULTILINE | re.DOTALL)
        outputString += separator + "Planned features" + separator + plannedFeatures

        # Formats titles
        outputString = re.sub(r"^##", "#", outputString, flags=re.MULTILINE)

        # Handles platform specific tags
        outputString = re.sub(r"@(.*?)@", r"\1", outputString, flags=re.MULTILINE | re.DOTALL)
        outputString = re.sub(r"\|.*?\|", r"", outputString, flags=re.MULTILINE | re.DOTALL)

        # Replace feedback section references to "Planned Features"
        outputString = re.sub(r"`[0-9]+?\. FEEDBACK`", r"*PLANNED FEATURES*", outputString, flags=re.MULTILINE)

        # Removes number for section redirection
        outputString = re.sub(r"`[0-9]+?\. (.*)?`", r"*\1*", outputString, flags=re.MULTILINE)

        #Output
        with open(outputFolder + "discord.txt", "w") as output:
            output.write(outputString)

def main():
    outputFolder =  "output\\"
    outputFileName = outputFolder + "creations.txt"
    if os.path.isfile(outputFileName):
        os.remove(outputFileName)
    outputFileName = outputFolder + "discord.txt"
    if os.path.isfile(outputFileName):
        os.remove(outputFileName)
    outputFileName = outputFolder + "nexus.txt"
    if os.path.isfile(outputFileName):
        os.remove(outputFileName)
    outputFileName = outputFolder + "readme.md"
    if os.path.isfile(outputFileName):
        os.remove(outputFileName)

    FormatNexusModPage(outputFolder)  
    FormatReadmeFile(outputFolder)
    FormatCreationsModPage(outputFolder)
    FormatDiscordTopics(outputFolder)

if __name__ == "__main__":
    main()