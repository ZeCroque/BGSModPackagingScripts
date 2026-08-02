import json
from pathlib import Path
import subprocess
import os
import shutil
import re
import glob

try:
    from . import papyrus_compiler
except ImportError:
    import papyrus_compiler

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

try:
    from . import utils
except ImportError:
    import utils


def GetVoicesFromAchList(achlist, mode, languageCode=""):
    filelist = ""
    with open(achlist, "r") as file:
        data = json.load(file)
        for f in data:        
            p = Path(f)
            if p.suffix == ".wem":
                if mode == "Xbox":
                    filelist += "Data\\Xbox\\" + str(Path(*p.parts[1:]))
                elif mode == "PS5":
                    filelist += "Data\\PS5\\" + str(Path(*p.parts[1:]))
                elif mode == "Localized":
                    filelist += "Data\\LocalizedVoices\\" + languageCode + "\\" + str(Path(*p.parts[1:]))
                else:
                    filelist += f
            else:
                filelist += f 
            filelist += "\n"
        filelist = filelist.rstrip('\n')
    return filelist

def GetFilesFromAchList(achList):
    filelist = ""
    try:
        with open(achList, "r") as file:
            data = json.load(file)
            for f in data:        
                filelist += f 
                filelist += "\n"
            filelist = filelist.rstrip('\n')
    except FileNotFoundError:
        return filelist
    return filelist

def InitFileList(fileListName, fileList, buildFolder):
    with open(buildFolder + fileListName, "w") as output:
        output.write(fileList)
        output.write("\n")

def AppendToFileList(fileListName, fileList, buildFolder):
    with open(buildFolder + fileListName, "a") as output:
        output.write(fileList)
        output.write("\n")

def PrepareFileListForAF(fileListName, buildFolder):
    with open(buildFolder + fileListName, 'r') as file:
        filedata = file.read()

    filedata = filedata.lower().replace(config.modNameLowerCase, config.modName + "_AF")

    with open(buildFolder + fileListName, 'w') as file:
        file.write(filedata)

def CopyFilesToBuildFolder(fileList, buildFolder, isAF=False):
    for file in fileList.splitlines():        
        dest = (buildFolder + os.path.dirname(file)).lower()        
        if isAF:        
            matches = re.findall(".*" + config.modNameLowerCase, dest)  
            if len(matches):
                dest = dest.replace(config.modNameLowerCase, config.modNameLowerCase + "_AF")
        matches = re.findall(".*(sound.*)", dest)  
        if(len(matches)):
            dest = buildFolder + "Data\\" + matches[0]

        os.makedirs(dest, exist_ok=True)
        shutil.copy(file, dest)

        if isAF:
            baseName = os.path.basename(file).lower()
            matches = re.findall(config.modNameLowerCase, baseName) 
            if len(matches):
                shutil.move(dest + "/" + baseName, dest + "/" + baseName.replace(config.modNameLowerCase, config.modName + "_AF"))

def CreateBA2(fileListName, archiveName, outputFolder):
    subprocess.run(["H:/Games/steamapps/common/Starfield/Tools/Archive2/Archive2.exe", "-s=" + fileListName, "-c=" + outputFolder + archiveName,  "-f=General", "-compression=None"], cwd='./build') 

def CreateLocalizedVoiceBA2(voiceList, voiceListPath, archiveNameBase, buildFolder, outputFolder):
    supportedLanguages = utils.GetAvailableLanguagesSuffixes(utils.Game(config.game))
    for supportedLanguage in supportedLanguages:
        if os.path.isdir("Data\\LocalizedVoices\\" + supportedLanguage):
            fileListName = supportedLanguage + ".txt"
            CopyFilesToBuildFolder(GetVoicesFromAchList(voiceListPath, "Localized", supportedLanguage), buildFolder)
            InitFileList(fileListName, voiceList, buildFolder)
            CreateBA2(fileListName, archiveNameBase + "Voices_" + supportedLanguage + ".ba2", outputFolder)
            os.remove(buildFolder + fileListName)

def CopyESMs(outputDir):
    esmPaths = glob.glob("./Data/*.esm")
    for esmPath in esmPaths:
        shutil.copy(esmPath, outputDir + esmPath)

def CopyFOMODFiles(outputDir):
    fomodFiles = glob.glob("./fomod/**/*.*", recursive=True)
    for fomodFile in fomodFiles:
        if os.path.isfile(fomodFile) and Path(fomodFile).suffix != ".in":
            dest = outputDir + os.path.dirname(fomodFile)
            os.makedirs(dest, exist_ok=True)
            shutil.copy(fomodFile, dest)
    thumbnailPath = config.modShortName + "_Thumbnail.png"
    if os.path.isfile(thumbnailPath):
        shutil.copy(thumbnailPath, outputDir)
    shutil.copy("readme.md", outputDir)

def CopyArtifactsToDataFolder(artifactsPath):
    artifacts = glob.glob(artifactsPath + "/Data/*")
    for artifact in artifacts:
        shutil.copy(artifact, "./Data/")

# ========================================================================

def CreateNexusArchive(mainFileList, modifiedVoiceList, vanillaVoiceList, vanillaVoiceListName, localizeVoices):
    buildName = "Nexus"
    artifactsSubpath = "artifacts\\" + buildName + "\\"
    artifactsFullpath = config.buildFolder + artifactsSubpath
    fileListName = buildName + ".txt"
    outputFolder =  "output\\"
    
    # Prepare build files
    CopyFilesToBuildFolder(mainFileList, config.buildFolder)
    CopyFilesToBuildFolder(vanillaVoiceList, config.buildFolder)
    CopyFilesToBuildFolder(modifiedVoiceList, config.buildFolder)

    if localizeVoices:
        # Main build
        InitFileList(fileListName, mainFileList, config.buildFolder) 
        CreateBA2(fileListName, config.mainArchiveName + config.archiveExtension, artifactsSubpath + "Data\\")
        os.remove(config.buildFolder + fileListName)
        
        # AI Voices
        if len(modifiedVoiceList) > 0:
            InitFileList(fileListName, vanillaVoiceList, config.buildFolder)
            AppendToFileList(fileListName, modifiedVoiceList, config.buildFolder)
            CreateBA2(fileListName, config.archiveNameBase + "Voices_en" + config.archiveExtension, artifactsSubpath + "Data\\")
            os.remove(config.buildFolder + fileListName)

        # NO AI Voices
        if len(vanillaVoiceList) > 0:
            InitFileList(fileListName, vanillaVoiceList, config.buildFolder)
            CreateBA2(fileListName, config.archiveNameBase + ("Voices_en_NO_AI" if len(modifiedVoiceList) > 0 else "Voices_en") + config.archiveExtension, artifactsSubpath + "Data\\")
            os.remove(config.buildFolder + fileListName)

        # Localized voices
        if len(vanillaVoiceList) > 0:
            CreateLocalizedVoiceBA2(vanillaVoiceList, vanillaVoiceListName, config.archiveNameBase, config.buildFolder, artifactsSubpath + "Data\\")
    else:
        InitFileList(fileListName, mainFileList, config.buildFolder) 
        if len(vanillaVoiceList) > 0:
            AppendToFileList(fileListName, vanillaVoiceList, config.buildFolder)
        CreateBA2(fileListName, config.mainArchiveName + config.archiveExtension, artifactsSubpath + "Data\\")

        if len(modifiedVoiceList) > 0:
            AppendToFileList(fileListName, modifiedVoiceList, config.buildFolder)
            CreateBA2(fileListName, config.mainArchiveName + "_NO_AI" + config.archiveExtension, artifactsSubpath + "Data\\")

        os.remove(config.buildFolder + fileListName)

    # Copy esms
    CopyESMs(artifactsFullpath)
    
    # Create zip
    CopyFOMODFiles(artifactsFullpath)
    
    # Output
    os.makedirs(outputFolder, exist_ok=True)
    shutil.make_archive(outputFolder + config.modName, 'zip', artifactsFullpath)

    # Cleanup
    shutil.rmtree(config.buildFolder + "Data")

def CreateCreationArchives(mainFileList, vanillaVoiceList, vanillaVoiceListName, isAF=False):
    buildName = "Creation"
    artifactsSubpath = "artifacts\\" + buildName + "\\"
    artifactsFullpath = config.buildFolder + artifactsSubpath
    fileListName = buildName + ".txt"
    archiveName = config.mainArchiveNameAF if isAF else config.mainArchiveName

    # Prepare common build files
    CopyFilesToBuildFolder(mainFileList, config.buildFolder, isAF)
    
    # Prepare file list
    InitFileList(fileListName, mainFileList, config.buildFolder)
    if len(vanillaVoiceList) > 0:
        AppendToFileList(fileListName, vanillaVoiceList, config.buildFolder) 
    if isAF:
        PrepareFileListForAF(fileListName, config.buildFolder)

    # PC build
    if os.path.isfile(vanillaVoiceListName):
        CopyFilesToBuildFolder(GetVoicesFromAchList(vanillaVoiceListName, "PC"), config.buildFolder, isAF)
    CreateBA2(fileListName, archiveName + config.archiveExtension, artifactsSubpath + "Data\\")

    # Xbox build
    if os.path.isfile(vanillaVoiceListName):
        CopyFilesToBuildFolder(GetVoicesFromAchList(vanillaVoiceListName, "Xbox"), config.buildFolder, isAF)
    CreateBA2(fileListName, archiveName + "_xbox" + config.archiveExtension, artifactsSubpath + "Data\\")

    # PS5 Build
    if os.path.isfile(vanillaVoiceListName):
        CopyFilesToBuildFolder(GetVoicesFromAchList(vanillaVoiceListName, "PS5"), config.buildFolder, isAF)
    CreateBA2(fileListName, archiveName + "_ps" + config.archiveExtension, artifactsSubpath + "Data\\")

    # Output
    CopyArtifactsToDataFolder(artifactsFullpath)
    if(isAF):
        shutil.copy("./Data/" + config.modName + ".esm", config.modFilePathAF)

    # Cleanup    
    os.remove(config.buildFolder + fileListName)
    shutil.rmtree(config.buildFolder + "Data")

def CreateArchives():
    mainFileList = GetFilesFromAchList("./Data/" + config.modShortName + "_Main.achlist")
    modifiedVoiceListName = "./Data/" + config.modShortName + "_ModdedVoices.achlist"
    modifiedVoiceList = GetFilesFromAchList(modifiedVoiceListName)
    vanillaVoiceListName = "./Data/" + config.modShortName + "_Voices.achlist"
    vanillaVoiceList = GetFilesFromAchList(vanillaVoiceListName)

    if os.path.isdir(config.buildFolder):
        shutil.rmtree(config.buildFolder)

    if os.path.isfile(config.modFilePathAF):
        os.remove(config.modFilePathAF)

    # Non-AF

    scriptsBuilt = False
    if(utils.AskForUserConfirm("Create nexus archive?")):
        localizeVoices = False
        if(vanillaVoiceList or modifiedVoiceList):
            localizeVoices = utils.AskForUserConfirm("Localize voices?")

        papyrus_compiler.FillTemplates(papyrus_compiler.CompileMode.DEFAULT)
        papyrus_compiler.Compile()
        scriptsBuilt = True

        CreateNexusArchive(mainFileList, modifiedVoiceList, vanillaVoiceList, vanillaVoiceListName, localizeVoices)

    if(utils.AskForUserConfirm("Prepare creation release?")):
        if(not scriptsBuilt):
            papyrus_compiler.FillTemplates(papyrus_compiler.CompileMode.DEFAULT)
            papyrus_compiler.Compile()
            scriptsBuilt = True

        CreateCreationArchives(mainFileList, vanillaVoiceList, vanillaVoiceListName, False)

    # AF
    if(utils.AskForUserConfirm("Prepare achievement-friendly release?")):
        papyrus_compiler.FillTemplates(papyrus_compiler.CompileMode.ACHIEVEMENT_FRIENDLY)
        papyrus_compiler.Compile()
        
        CreateCreationArchives(mainFileList, vanillaVoiceList, vanillaVoiceListName, True)

def main():   
    CreateArchives()

if __name__ == "__main__":
    main()