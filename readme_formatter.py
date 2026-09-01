import re
import json

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

capturedSections = []
def EraseAndCapture(m):
    capturedSections.append(m.group(1))
    return m.group(2)

def FormatCreationsModPage(outputFolder):
    with open("./readme.md", "r") as input:
        inputString = input.read()
        sectionsToKeep = [1, 2]
        try:
            with open("./creationsModpageSections.json", "r") as file:
                indexes = json.load(file)
                for index in indexes:
                    sectionsToKeep.append(int(index))
        except FileNotFoundError: 
            utils.AskForUserConfirm("The creationsModpageSections.json file is missing, only OVERVIEW and DETAILS will be kept. Continue?")

        # Removes all before first section
        outputString = re.sub(r"#.*?## Index.*?##", r"##", inputString, flags=re.MULTILINE | re.DOTALL)

        # Extracts sections
        while True:
            outputString, count = re.subn(r"(## [0-9]+?\. .*?)(^## [0-9])+?", EraseAndCapture, outputString, count=1, flags=re.MULTILINE | re.DOTALL)
            if not count:
                break
        capturedSections.append(outputString)

        # Cherry picks sections
        outputString = ""
        i = 1
        for index in sectionsToKeep:
            outputString += re.sub(r"^## [0-9]+?\.", "## " + str(i) + ".", capturedSections[index - 1])
            i += 1

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
