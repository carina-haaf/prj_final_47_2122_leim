
# TESTE SOBRE UM VIDEOO NOVO PARA PROCESSO DE CONSTRUÇÃO DAS PASTAS A SEREM USADAS
# NA VISUALIZAÇÃO DOS RESULTADOS

# =================================================================================
# Imports ...
# =================================================================================
import testDatasetConstructor
from additional.videoProcessing import *
from additional.constants import *
from additional.processCsvFile import *
from additional.directoryManipulator import *
import testDatasetConstructor


# hyper parameters
nog = NOG  # number of groups
spr = SPG  # samples per group
nof = NOF  # number of features
noss = NOSS  # number of shifted samples

# =================================================================================
# obter dataset para videos a serem utilizados na aplicação
# do modelo a dados novos....
# =================================================================================

clear_dir(TEST_AUDIO_PATH)

file_rows = list()

CsvFile.remove_file("../" + TEST_DIR_PATH + "/" + TEST_DATASET_PATH)
features_file = CsvFile(TEST_DIR_PATH + "/" + TEST_DATASET_PATH, "w")

# v = Video(TEST_VIDEO_PATH + "/", TEST_VIDEO_NAME)
# video = v.get_file()

# testDatasetConstructor.construct(nog, spr, noss, features_file, file_rows, video)


paths_train = [TEST_VIDEO_PATH, TEST_AUDIO_PATH]
testDatasetConstructor.construct(paths_train, nog, spr,
                                 noss, features_file, file_rows)
