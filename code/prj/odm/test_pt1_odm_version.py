
# =================================================================================
# Imports ...
# =================================================================================
from odm import odmDatasetConstructor
from processing.directoryManipulator import *
from processing.processCsvFile import *


# hyper parameters
nog = 5  # number of groups
spr = 4096  # samples per group
nof = 3  # number of features
noss = 4096  # number of shifted samples

# =================================================================================
# obter dataset para videos a serem utilizados no treino do modelo....
# =================================================================================

clear_dir("../audios")

file_rows = list()
CsvFile.remove_file("../odm/odm_features_file.csv")
features_file = CsvFile("odm/odm_features_file.csv", "w")


features_file = odmDatasetConstructor.construct_3row_header_format(features_file, nof, nog)
paths_train = ["../videos", "../audios"]
odmDatasetConstructor.construct(paths_train, nog, spr, noss, features_file, file_rows)




