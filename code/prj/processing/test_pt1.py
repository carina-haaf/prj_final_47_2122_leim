
# =================================================================================
# Imports ...
# =================================================================================
from processing import datasetConstructor
from processing.directoryManipulator import *

nog = 21  # number of groups
spr = 1024  # samples per group
nof = 3  # number of features
noss = 1024  # number of sifted samples


# =================================================================================
# obter dataset para videos a serem utilizados no treino do modelo....
# =================================================================================

clear_dir("../audios/dataset/train")

file_rows = list()
features_file = datasetConstructor.set_up_features_file("processing/features_file.csv")

paths_train = ["../videos/train", "../audios/dataset/train"]
datasetConstructor.construct(paths_train, nog, spr, noss, features_file, file_rows)


# =================================================================================
# obter dataset para videos a serem classificados pelo modelo....
# =================================================================================

clear_dir("../audios/dataset/classification")

file_rows = list()
features_file = datasetConstructor.set_up_features_file("processing/features_classif_file.csv")

paths_classification = ["../videos/classification", "../audios/dataset/classification"]
datasetConstructor.construct(paths_classification, nog, spr, noss, features_file, file_rows)

