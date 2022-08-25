# teste parecido com o test_pt2.py, mas neste caso carrega um modelo já treinado
# =================================================================================
# imports...
# =================================================================================

from processing import datasetConstructor
from processing.videoProcessing import *
from processing.processCsvFile import *
from filesManipulator.file import *

from pandas import read_csv
import numpy as np

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from keras.models import load_model
import time

# =================================================================================
# Iniciar contagem de tempo de processamento ...
# =================================================================================

start = time.time()
print("The program is running...")

# =================================================================================
# Definição do dataset ...
# =================================================================================


def organize_info(info_array):
    string = ""
    size = len(info)

    for i in range(size):
        if i == size - 1:
            string += str(info_array[i]) + "\n"
        else:
            string += str(info_array[i]) + ";"
    return string


dataset = read_csv("features_test_file.csv", header=None)
X, Y = datasetConstructor.get_features_and_label_values(dataset, debug=True)

# scaler = MinMaxScaler(feature_range=(0, 1))
# transform data
# X = scaler.fit_transform(X)
# print(X_scaled)

# Load model
model = load_model('../models/constructed_models/model_127')
model.summary()


print("\n\nModel Summary: ")
print(model.summary())

y_predict = model.predict(X)
y_predict = np.where(y_predict > 0.5, 1, 0)
# print(np.unique(y_predict))

# generate mini clips

nog = 22  # number of groups
spr = 1024  # samples per group
nof = 3  # number of features
noss = 1024  # number of sifted samples

video_name = "vid_20_08_2022_17_22"
path = "mini_clips/" + video_name + "/clips_info/clips_info.txt"
File.remove_file("../" + path)
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

"""

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




"""


end = time.time()
#  dif = (end - start)/60
dif = end - start
print('Processing time: ', np.round_(dif, 0), "seconds")

