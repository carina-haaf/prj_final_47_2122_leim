# teste parecido com o constructAndTrainModelWithCV.py, mas neste caso carrega um modelo já treinado
# =================================================================================
# imports...
# =================================================================================

from model import modelManipulator
from additional.videoProcessing import *
from additional.file import *
from additional.constants import *
from additional import directoryManipulator

from pandas import read_csv
import numpy as np

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from keras.models import load_model
import time
from os.path import exists

import operator

import sklearn.preprocessing as pp
from sklearn.decomposition import PCA

# =================================================================================
# Iniciar contagem de tempo de processamento ...
# =================================================================================

start = time.time()
print("The program is running...")


def organize_info(info_array):
    string = ""
    size = len(info)

    for i in range(size):
        if i == size - 1:
            string += str(info_array[i]) + "\n"
        else:
            string += str(info_array[i]) + ";"
    return string

# =================================================================================
# Load dataset ...
# =================================================================================


dataset = read_csv(TEST_DATASET_PATH, header=None)
X, Y = modelManipulator.get_features_and_label_values(dataset, debug=True)
#X = pp.normalize(X)

# =================================================================================
# Load model ...
# =================================================================================

model = load_model("../" + MODEL_PATH + "/" + TRAINED_MODELS_PATH + '/model_' + str(CHOSE_MODEL))

print("\n\nModel Summary: ")
print(model.summary())


# =================================================================================
# Events Classification Results ...
# =================================================================================
y_predict_ini = model.predict(X)
print(np.unique(y_predict_ini))
y_predict = np.where(y_predict_ini > DECISION_LIMIT, 1, 0)
#print(np.unique(y_predict))

print("\n\n# =================================================================================")
print("                         V A L I D A T I O N    R E S U L T S")
print("# =================================================================================")

print("\n\nConfusion Matrix: ")
print(confusion_matrix(Y, y_predict))  # order matters! (actual, predicted)

print("\n\nClassification Report: ")
print(classification_report(Y, y_predict, target_names=["noise", "hit"]))

loss, accuracy = model.evaluate(X, Y, verbose=0)

print("\n\nEvaluation Matrics:")
print("Accuracy: ", accuracy)
print("Loss: ", loss)


# =================================================================================
# Create directories and files ...
# =================================================================================
file_exists = exists(MINI_CLIPS_VIDEO_NAME_PATH)
if file_exists:
    print("The mini clips video file you trying to create "
          "already exists.\nChange the 'MINI_CLIPS_VIDEO_NAME' variable"
          "'additional.constants.py' file. ")
    # exit(0)


# create directories
video_clip_name = MINI_CLIPS_VIDEO_NAME
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH)
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH + "/clips")
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH + "/dataset")
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH + "/userAnalysis")

# create and write on dataset_classes.txt file
File.remove_file(MINI_CLIPS_INFO_PATH_TO_REMOVE)  # remove clips_info.txt file
infoFile = File(MINI_CLIPS_INFO_PATH_TO_CREATE)  # create new clips_info.txt file
# create and write on dataset_classes.txt file
File.remove_file(MINI_CLIPS_INFO_NON_SORTED_PATH_TO_REMOVE)  # remove clips_info.txt file
infoFileNonSorted = File(MINI_CLIPS_INFO_NON_SORTED_PATH_TO_CREATE)  # create new clips_info.txt file

# create and write on dataset_classes.txt file
File.remove_file(DATASET_CLASSES_PATH_TO_REMOVE)  # remove dataset_classes.txt file
dataset_classes_file = File(DATASET_CLASSES_PATH_TO_CREATE)  # create new dataset_classes.txt file
dataset_classes_file.write(["ball-hit;noise"])

# create and write on readme.txt file
File.remove_file(README_TO_REMOVE)  # remove readme.txt file
readme_file = File(README_TO_CREATE)  # create new readme.txt file
readme_file.write(["clips_info.txt file format:\nindice_do_clip;amostra_inicial;amostra_final;"
                   "tempo_inicial,tempo_final;tipo_batida;nome_clip;probabilidade"])


# =================================================================================
# # sort mini clips by prob on y predicted array ...
# =================================================================================

nog = NOG  # number of groups
spr = SPG  # samples per group
nof = NOF  # number of features
noss = NOSS  # number of shifted samples

D = {}
for j in range(y_predict.shape[0]):
    ini_idx = j * noss
    final_idx = j * noss + (nog * spr)

    ini = get_time(ini_idx)
    final = get_time(final_idx)
    # print(j, ini_idx, final_idx, ini, final)

    event_type = "ball-hit" if y_predict[j] == 1 else "noise"

    prob = str(y_predict_ini[j]).split("[")[1].split("]")[0]
    info = ini_idx, final_idx, ini, final, event_type, prob
    data = organize_info(info)
    D[data] = y_predict_ini[j]

    newclip_event_type = "ball_hit" if event_type == "ball-hit" else "noise"
    newclip_name = "clip_" + str(j) + "_" + newclip_event_type + ".mp4"

    fileLine = j, ini_idx, final_idx, ini, final, event_type, newclip_name, prob
    fileLineData = organize_info(fileLine)
    infoFileNonSorted.write([fileLineData])


sorted_dict = dict(sorted(D.items(), key=operator.itemgetter(1), reverse=True))


# =================================================================================
# # generate mini clips ...
# =================================================================================

index = 0
for k in sorted_dict:

    info = k
    splited_info = info.split(";")

    ini_idx = splited_info[0]
    final_idx = splited_info[1]
    ini = splited_info[2]
    final = splited_info[3]
    event_type = splited_info[4]
    prob = splited_info[5]
    prob = prob.replace("\n", "")

    #newclip = mp.VideoFileClip("../test/test_videos/" + TEST_VIDEO_NAME).subclip(ini, final)
    newclip_event_type = "ball_hit" if event_type == "ball-hit" else "noise"
    newclip_name = "clip_" + str(index) + "_" + newclip_event_type + ".mp4"
    #newclip.write_videofile("mini_clips/" + video_clip_name + "/clips" + "/" + newclip_name)

    info = index, ini_idx, final_idx, ini, final, event_type, newclip_name, prob
    data = organize_info(info)
    infoFile.write([data])

    index += 1


lines = infoFile.read()
print(lines)


# =================================================================================
# Terminar contagem de tempo de processamento ...
# =================================================================================


end = time.time()
#  dif = (end - start)/60
dif = end - start
print('Processing time: ', np.round_(dif, 0), "seconds")
