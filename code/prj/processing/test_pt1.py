
# =================================================================================
# Imports ...
# =================================================================================
from processing import datasetConstructor
from processing.directoryManipulator import *
from processing.processCsvFile import *


# hyper parameters
nog = 21  # number of groups
spr = 1024  # samples per group
nof = 3  # number of features
noss = 2048  # number of sifted samples


# =================================================================================
# obter dataset para videos a serem utilizados no treino do modelo....
# =================================================================================

clear_dir("../audios")

file_rows = list()
CsvFile.remove_file("../processing/features_file.csv")
features_file = datasetConstructor.create_file("processing/features_file.csv")

paths_train = ["../videos", "../audios"]
datasetConstructor.construct(paths_train, nog, spr, noss, features_file, file_rows)

#print("Lines: ", len(file_rows))
#print("Columns: ", len(file_rows[0]))






