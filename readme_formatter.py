import re
import json
import os
import shutil

try:
    from . import utils
except ImportError:
    import utils

def ParseSpecialMarking(inputString, keepNexus, keepCreations, keepAF):
    outputString = re.sub(r"@(.*?)@", r"\1" if keepNexus else r"", inputString, flags=re.MULTILINE | re.DOTALL)
    outputString = re.sub(r"\|(.*?)\|", r"\1" if keepCreations else r"", outputString, flags=re.MULTILINE | re.DOTALL)
    outputString = re.sub(r"<(.*)?>", r"\1" if keepAF else r"", outputString, flags=re.MULTILINE | re.DOTALL)
    return outputString

footer = ""
def FooterEraseAndCapture(m):
    global footer
    footer = m.group(1)
    return ""

def FormatNexusModPage(outputFolder):
    with open("./ModPage/readme.md", "r") as input:
        inputString = input.read()

        # Save header
        header = re.match(r"# (.*)\n##.*?Feedback\n(.*?)\n##", inputString, flags=re.MULTILINE | re.DOTALL)

        # Removes index
        outputString = re.sub(r"#.*## Index.*?##", r"##", inputString, flags=re.MULTILINE | re.DOTALL)

        # Parse and restore header
        hook = ParseSpecialMarking(header.group(2), True, False, False)
        if len(hook) > 1:
            hook += "\n\n"
        outputString =  "# " + header.group(1) + "\n" + hook + outputString

        # Save and remove footer
        outputString = re.sub(r"CREATIONS_FOOTER\n(.*)CREATIONS_FOOTER_END", FooterEraseAndCapture, inputString, flags=re.MULTILINE | re.DOTALL)

        # Handles platform specific tags
        outputString = ParseSpecialMarking(outputString, True, False, False)

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

        # Outputs
        with open(outputFolder + "nexus.txt", "w") as output:
            output.write(outputString)

def FormatReadmeFile(outputFolder):
    with open("./ModPage/readme.md", "r") as input:
        inputString = input.read()

        # Save and remove footer
        inputString = re.sub(r"CREATIONS_FOOTER\n(.*)CREATIONS_FOOTER_END", FooterEraseAndCapture, inputString, flags=re.MULTILINE | re.DOTALL)

        # Handles platform specific tags
        outputString = ParseSpecialMarking(inputString, True, False, False)

        # Outputs
        with open(outputFolder + "readme.md", "w") as output:
            output.write(outputString)

capturedSections = {}
def EraseAndCapture(m):
    capturedSections[m.group(2)] = m.group(1)
    return m.group(3)

def ExtractSections(inputString):
    # Removes all before first section
    outputString = re.sub(r"#.*?## Index.*?Feedback\n", r"", inputString, flags=re.MULTILINE | re.DOTALL)
    
    # Save the text between the index and the first section
    header = re.sub(r"##.*", r"", outputString, flags=re.MULTILINE | re.DOTALL)

    # Extracts sections
    while True:
        outputString, count = re.subn(r"(## [0-9]+?\. (.*?)\r?\n.*?)(^## [0-9])+?", EraseAndCapture, outputString, count=1, flags=re.MULTILINE | re.DOTALL)
        if not count:
            break
    capturedSections["FEEDBACK"] = outputString
    return header

def PickSections(titles):
    outputString = ""
    i = 1
    for title in titles:
        if title in capturedSections:
            outputString += re.sub(r"^## [0-9]+?\. (.*)", "## " + str(i) + r". \1" if len(titles) > 1 else "", capturedSections[title])
            i += 1
    return outputString

def FormatCreationsModPage(outputFolder, isAF):
    with open("./ModPage/readme.md", "r") as input:
        inputString = input.read()

        # Save and remove footer
        inputString = re.sub(r"CREATIONS_FOOTER\n(.*)CREATIONS_FOOTER_END", FooterEraseAndCapture, inputString, flags=re.MULTILINE | re.DOTALL)

        sectionsToKeep = ["OVERVIEW", "DETAILS"]
        try:
            with open("./creationsModpageSections.json", "r") as file:
                titles = json.load(file)
                for title in titles:
                    sectionsToKeep.append(title)
        except FileNotFoundError: 
            utils.AskForUserConfirm("The creationsModpageSections.json file is missing, only OVERVIEW and DETAILS will be kept. Continue?")

        # Extracts and parse header, then append selected sections to the result
        header = ExtractSections(inputString) 
        header = ParseSpecialMarking(header, False, True, isAF)
        outputString = ("" if len(header) == 1 else header + "\n") + PickSections(sectionsToKeep)

        # Handles platform specific tags
        outputString = ParseSpecialMarking(outputString, False, True, isAF)

        # Formats titles
        outputString = re.sub(r"^##", "#", outputString, flags=re.MULTILINE)

        # Handles URLs
        outputString = re.sub(r"\[([^]]*?)\]\(.*?\)", r"\1", outputString, flags=re.MULTILINE)

        # Adds creations footer
        outputString += "# " + str(len(sectionsToKeep) + 1) + footer

        #Output
        with open(outputFolder + "creations" + ("_af" if isAF else "") + ".txt", "w") as output:
            output.write(outputString)

def FormatDiscordTopics(outputFolder):
    with open("./ModPage/readme.md", "r") as input:
        inputString = input.read()

        # Save and remove footer
        inputString = re.sub(r"CREATIONS_FOOTER\n(.*)CREATIONS_FOOTER_END", FooterEraseAndCapture, inputString, flags=re.MULTILINE | re.DOTALL)

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

        # Handles platform specific tags
        outputString = ParseSpecialMarking(outputString, True, False, False)

        # Formats titles
        outputString = re.sub(r"^##", "#", outputString, flags=re.MULTILINE)

        # Replace feedback section references to "Planned Features"
        outputString = re.sub(r"`[0-9]+?\. FEEDBACK`", r"*PLANNED FEATURES*", outputString, flags=re.MULTILINE)

        # Removes number for section redirection
        outputString = re.sub(r"`[0-9]+?\. (.*)?`", r"*\1*", outputString, flags=re.MULTILINE)

        #Output
        with open(outputFolder + "discord.txt", "w") as output:
            output.write(outputString)

def main():
    outputFolder =  "output\\"
    os.makedirs(outputFolder, exist_ok=True)

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
    FormatCreationsModPage(outputFolder, True)
    FormatCreationsModPage(outputFolder, False)
    FormatDiscordTopics(outputFolder)

    # Update git readme
    shutil.copy(outputFileName, "./")

if __name__ == "__main__":
    main()