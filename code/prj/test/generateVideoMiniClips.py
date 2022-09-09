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
import pickle


# =================================================================================
# Auxiliary method ...
# =================================================================================

def organize_info(info_array):
    string = ""
    size = len(info_array)

    for i in range(size):
        if i == size - 1:
            string += str(info_array[i]) + "\n"
        else:
            string += str(info_array[i]) + ";"
    return string


# =================================================================================
# Show info ...
# =================================================================================

print("\n\nChosen Experiment: ", EXPERIMENT)
print("Samples per group: ", SPG)
print("\n\n\n")

# =================================================================================
# Initiate time counter ...
# =================================================================================

start = time.time()
print("The program is running...")


# =================================================================================
# Load dataset ...
# =================================================================================

dataset = read_csv(TEST_DATASET_PATH, header=None)
X_non_scaled, Y = modelManipulator.get_features_and_label_values(dataset, debug=True)


# =================================================================================
# Data pre-processing ...
# =================================================================================

scaler = None
if CV_MODE:
    # get scaler from models constructed with CV
    scaler = pickle.load(open("../" + MODEL_PATH + "/" + TRAINED_MODELS_PATH +
                              '/exp_' + str(EXPERIMENT) + '/scaler_' + str(CHOSE_MODEL) + ".pkl", 'rb'))
else:
    # get scaler from models constructed with all dataset
    scaler = pickle.load(open("../" + MODEL_PATH + "/" + TRAINED_MODELS_WITH_ALL_DATA_PATH +
                              '/model_' + str(EXPERIMENT) + '/scaler_' + str(EXPERIMENT) + ".pkl", 'rb'))

X = scaler.transform(X_non_scaled)


# =================================================================================
# Load model ...
# =================================================================================

if CV_MODE:
    # get model constructed using CV
    model = load_model("../" + MODEL_PATH + "/" + TRAINED_MODELS_PATH +
                       '/exp_' + str(EXPERIMENT) + '/model_' + str(CHOSE_MODEL))
else:
    # get model constructed using all dataset
    model = load_model("../" + MODEL_PATH + "/" + TRAINED_MODELS_WITH_ALL_DATA_PATH +
                       '/model_' + str(EXPERIMENT) + '/trained_model_' + str(EXPERIMENT))

print("\n\nModel Summary: ")
print(model.summary())


# =================================================================================
# Events Classification Results ...
# =================================================================================

y_predict_ini = model.predict(X)
print(np.unique(y_predict_ini))
y_predict = np.where(y_predict_ini > DECISION_LIMIT, 1, 0)
# print(np.unique(y_predict))


print("\n\n# =================================================================================")
print("                         T E S T    R E S U L T S")
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
    exit(0)


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
File.remove_file(MINI_CLIPS_INFO_NON_SORTED_PATH_TO_REMOVE)  # remove clips_info_non_sorted.txt file
infoFileNonSorted = File(MINI_CLIPS_INFO_NON_SORTED_PATH_TO_CREATE)  # create new clips_info_non_sorted.txt file

# create and write on dataset_classes.txt file
File.remove_file(DATASET_CLASSES_PATH_TO_REMOVE)  # remove dataset_classes.txt file
dataset_classes_file = File(DATASET_CLASSES_PATH_TO_CREATE)  # create new dataset_classes.txt file
dataset_classes_file.write(["ball-hit;noise"])

# create and write on readme.txt file
File.remove_file(README_TO_REMOVE)  # remove readme.txt file
readme_file = File(README_TO_CREATE)  # create new readme.txt file
readme_file.write(["clips_info.txt file format:\nindice_do_clip;amostra_inicial;amostra_final;"
                   "tempo_inicial,tempo_final;tipo_de_evento;nome_clip;probabilidade_associada_ah_detecao_do_evento"])


# =================================================================================
# # generate mini clips ...
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

    newclip = mp.VideoFileClip("../test/test_videos/" + TEST_VIDEO_NAME).subclip(ini, final)
    newclip_event_type = "ball_hit" if event_type == "ball-hit" else "noise"
    newclip_name = "clip_" + str(j) + "_" + newclip_event_type + ".mp4"
    newclip.write_videofile("mini_clips/" + video_clip_name + "/clips" + "/" + newclip_name)

    prob = str(y_predict_ini[j]).split("[")[1].split("]")[0]
    info = ini_idx, final_idx, ini, final, event_type, newclip_name, prob
    data = organize_info(info)
    D[data] = y_predict_ini[j]

    fileLine = j, ini_idx, final_idx, ini, final, event_type, newclip_name, prob
    print(fileLine)
    fileLineData = organize_info(fileLine)
    infoFileNonSorted.write([fileLineData])


# =================================================================================
# # write clips info sorted by probability on clips_info.txt file ...
# =================================================================================

sorted_dict = dict(sorted(D.items(), key=operator.itemgetter(1), reverse=True))

index = 0
for k in sorted_dict:

    info = k
    splited_info = info.split(";")

    ini_idx = splited_info[0]
    final_idx = splited_info[1]
    ini = splited_info[2]
    final = splited_info[3]
    event_type = splited_info[4]
    new_clip_name = splited_info[5]
    prob = splited_info[6]
    prob = prob.replace("\n", "")

    newclip_name = new_clip_name

    info = index, ini_idx, final_idx, ini, final, event_type, newclip_name, prob
    print(info)
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


from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt
ConfusionMatrixDisplay.from_predictions(Y, y_predict, cmap=plt.cm.Blues)
plt.show()

