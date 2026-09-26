import os

try:
    from . import translator
except ImportError:
    import translator

try:
    from . import ba2_creator
except ImportError:
    import ba2_creator

try:
    from . import utils
except ImportError:
    import utils

try:
    from . import mo2
except ImportError:
    import mo2

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

def ClearArchives(isAF):
    archiveName = config.mainArchiveNameAF if isAF else config.mainArchiveName

    fullArchivePath = "./Data/" + archiveName + config.archiveExtension
    if os.path.isfile(fullArchivePath):
        os.remove(fullArchivePath)

    fullArchivePath = "./Data/" + archiveName + "_xbox" + config.archiveExtension
    if os.path.isfile(fullArchivePath):
        os.remove(fullArchivePath)

    fullArchivePath = "./Data/" + archiveName + "_ps" + config.archiveExtension
    if os.path.isfile(fullArchivePath):
        os.remove(fullArchivePath)

def Package():   
    if utils.AskForUserConfirm("Would you like to localize the .esm?"):
        translator.Translate()
        ClearArchives(True)
        ClearArchives(False)
        mo2.RunMO2Target("xTranslator")
        if(not utils.AskForUserConfirm(".esm localized. Proceed to archive creation?")):
            return

    if(os.path.isfile(config.modShortName + "_Thumbnail.png") or utils.AskForUserConfirm("Thumbnail file not found. Proceed anyway?")):
        ba2_creator.CreateArchives()

def main():
    Package()

if __name__ == "__main__":
    main()