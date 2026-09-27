import shutil
import os

try:
    from . import mo2
except ImportError:
    import mo2

try:
    from .mod_info import config
except ImportError:
    from mod_info import config

def GenerateSEQ():
    mo2.RunCKWithArgs("-GenerateSEQ:" + config.modName + ".esp")

    seqPath = config.gamePath + "/" + config.modName + ".SEQ"
    shutil.copy(seqPath, "./Data/SEQ/" + config.modName + ".seq")
    os.remove(seqPath)

def main():
    GenerateSEQ()

if __name__ == "__main__":
    main()