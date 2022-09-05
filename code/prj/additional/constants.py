from datetime import datetime

# CONSTANTS

# temporal hyper parameters
NOG = 22  # number of groups
SPG = 1024  # samples per group
NOF = 3  # number of features
NOSS = 1024  # number of shifted samples

PERCENTAGE = 0.7

# NN hyper parameters
LR = 0.001  # learning rate
NR_EPOCHS = 200
BATCH_SIZE = 128
LOSS_FUNCTION = "binary_crossentropy"  # "binary_crossentropy"
DECISION_LIMIT = 0.5  # to decide whether it is a ball hit or noise
NR_OF_INPUT_LAYER_NODES = NOG * NOF
OUTPUT_ACTIVATION_FUNCTION = "sigmoid"
HIDDEN_LAYERS_ACTIVATION_FUNCTION = "relu"

# Cross validation
NR_KFOLDS = 5

# chose classifier / model on test process
EXPERIMENT = 20
CHOSE_MODEL = 1

# directories path
AUDIOS_PATH = "../../data/audios"
VIDEOS_PATH = "../../data/videos"
TRAINED_MODELS_PATH = "trained_models/constructed_models"
TRAINED_MODELS_GRAPHS_PATH = "trained_models/models_graphs"
TEST_VIDEO_PATH = "./test_videos"
TEST_AUDIO_PATH = "./test_audios"
TEST_DIR_PATH = "test"
MODEL_PATH = "model"

# files path
ODM_DATASET_PATH = "../data/odm_features_file.csv"
MAIN_DATASET_PATH = "data/features_file.csv"
TEST_DATASET_PATH = "features_test_file.csv"
LABELING_FILES_PATH = "../data/labeling"
LABELING_TEST_FILES_PATH = "dataset/data/labeling"


# test video name
TEST_VIDEO_NAME = "padel_137.mp4"
MINI_CLIPS_VIDEO_NAME = "vid_" + datetime.today().strftime('%d_%m_%Y_%H_%M_%S')

MINI_CLIPS_VIDEO_NAME_PATH = "mini_clips/" + MINI_CLIPS_VIDEO_NAME
MINI_CLIPS_INFO_PATH_TO_REMOVE = MINI_CLIPS_VIDEO_NAME_PATH + "/clips_info.txt"
MINI_CLIPS_INFO_PATH_TO_CREATE = "test/" + MINI_CLIPS_VIDEO_NAME_PATH + "/clips_info.txt"
DATASET_CLASSES_PATH_TO_REMOVE = MINI_CLIPS_VIDEO_NAME_PATH + "/dataset/dataset_classes.txt"
DATASET_CLASSES_PATH_TO_CREATE = "test/" + MINI_CLIPS_VIDEO_NAME_PATH + "/dataset/dataset_classes.txt"
MINI_CLIPS_INFO_NON_SORTED_PATH_TO_REMOVE = "test/" + MINI_CLIPS_VIDEO_NAME_PATH + "/clips_info_non_sorted.txt"
MINI_CLIPS_INFO_NON_SORTED_PATH_TO_CREATE = "test/" + MINI_CLIPS_VIDEO_NAME_PATH + "/clips_info_non_sorted.txt"
README_TO_REMOVE = MINI_CLIPS_VIDEO_NAME_PATH + "/readme.txt"
README_TO_CREATE = "test/" + MINI_CLIPS_VIDEO_NAME_PATH + "/readme.txt"
