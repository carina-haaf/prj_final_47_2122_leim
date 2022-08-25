
# TESTE SOBRE UM VIDEOO NOVO PARA PROCESSO DE CONSTRUÇÃO DAS PASTAS A SEREM USADAS
# NA VISUALIZAÇÃO DOS RESULTADOS

# =================================================================================
# Imports ...
# =================================================================================
from processing import datasetConstructor
from processing import videoClassifier
from processing.videoProcessing import *
from processing.directoryManipulator import *
from processing.processCsvFile import *


# hyper parameters
nog = 22  # number of groups
spr = 1024  # samples per group
nof = 3  # number of features
noss = 1024  # number of sifted samples

# =================================================================================
# obter dataset para videos a serem utilizados no treino do modelo....
# =================================================================================

clear_dir("../test_audios")

file_rows = list()
CsvFile.remove_file("../processing/features_test_file.csv")
features_file = videoClassifier.create_file("processing/features_test_file.csv")

v = Video("../test_videos", "padel_58.mp4")
video = v.get_file()
videoClassifier.construct(nog, spr, noss, features_file, file_rows, video)








