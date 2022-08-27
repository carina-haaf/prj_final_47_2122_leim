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
# Definição do dataset ...
# =================================================================================


dataset = read_csv(TEST_DATASET_PATH, header=None)
X, Y = modelManipulator.get_features_and_label_values(dataset, debug=True)

# Load model
model = load_model("../" + MODEL_PATH + "/" + TRAINED_MODELS_PATH + '/model_' + str(CHOSE_MODEL))

print("\n\nModel Summary: ")
print(model.summary())

y_predict = model.predict(X)
y_predict = np.where(y_predict > DECISION_LIMIT, 1, 0)
# print(np.unique(y_predict))

# generate mini clips

nog = NOG  # number of groups
spr = SPG  # samples per group
nof = NOF  # number of features
noss = NOSS  # number of shifted samples

file_exists = exists(MINI_CLIPS_VIDEO_NAME_PATH)
if file_exists:
    print("The mini clips video file you trying to create "
          "already exists.\nChange the 'MINI_CLIPS_VIDEO_NAME' variable"
          "'additional.constants.py' file. ")
    #exit(0)


# create directories
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH)
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH + "/clips_info")
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH + "/hits")
directoryManipulator.create_dir(MINI_CLIPS_VIDEO_NAME_PATH + "/noise")


video_name = MINI_CLIPS_VIDEO_NAME
path = MINI_CLIPS_INFO_PATH

File.remove_file(path)
infoFile = File(path)

for j in range(y_predict.shape[0]):
    ini_idx = j * noss
    final_idx = j * noss + (nog * spr)

    ini = get_time(ini_idx)
    final = get_time(final_idx)
    # print(j, ini_idx, final_idx, ini, final)

    # newclip = mp.VideoFileClip("../test_videos/padel_58.mp4").subclip(ini, final)
    event_type = "ball-hit" if y_predict[j] == 1 else "noise"
    newclip_event_type = "ball_hit" if y_predict[j] == 1 else "noise"
    newclip_name = "clip_" + str(j) + "_" + newclip_event_type + ".mp4"
    # newclip.write_videofile("../mini_clips/" + event_type + "/newclip_name")

    info = j, ini_idx, final_idx, ini, final, event_type, newclip_name
    data = organize_info(info)
    infoFile.write([data])

lines = infoFile.read()
print(lines)



print("\n\n# =================================================================================")
print("                         V A L I D A T I O N    R E S U L T S")
print("# =================================================================================")

print("\n\nConfusion Matrix: ")
print(confusion_matrix(Y, y_predict))  # order matters! (actual, predicted)

print("\n\nClassification Report: ")
print(classification_report(Y, y_predict))

loss, accuracy = model.evaluate(X, Y, verbose=0)

print("\n\nEvaluation Matrics:")
print("Accuracy: ", accuracy)
print("Loss: ", loss)

# =================================================================================
# Terminar contagem de tempo de processamento ...
# =================================================================================


end = time.time()
#  dif = (end - start)/60
dif = end - start
print('Processing time: ', np.round_(dif, 0), "seconds")

