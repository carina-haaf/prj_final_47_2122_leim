
# =================================================================================
# Imports ...
# =================================================================================
from dataset.construct.mainVersion import datasetConstructor
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
CsvFile.remove_file("../../" + MAIN_DATASET_PATH)
features_file = CsvFile("../" + MAIN_DATASET_PATH, "w")


paths_train = [VIDEOS_PATH, AUDIOS_PATH]
datasetConstructor.construct(paths_train, nog, spr, noss, features_file, file_rows)

# print("Lines: ", len(file_rows))
# print("Columns: ", len(file_rows[0]))
