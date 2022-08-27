
# =================================================================================
# Imports ...
# =================================================================================
from dataset.construct.odmVersion import odmDatasetConstructor
from additional.directoryManipulator import *
from additional.processCsvFile import *
from additional.constants import *


# hyper parameters
nog = NOG  # number of groups
spr = SPG  # samples per group
nof = NOF  # number of features
noss = NOSS  # number of shifted samples

# =================================================================================
# obter dataset para videos a serem utilizados no treino do modelo....
# =================================================================================

clear_dir(AUDIOS_PATH)

file_rows = list()
CsvFile.remove_file("../" + ODM_DATASET_PATH)
features_file = CsvFile(ODM_DATASET_PATH, "w")


features_file = odmDatasetConstructor.construct_3row_header_format(features_file, nof, nog)
paths_train = [VIDEOS_PATH, AUDIOS_PATH]
odmDatasetConstructor.construct(paths_train, nog, spr, noss, features_file, file_rows)
