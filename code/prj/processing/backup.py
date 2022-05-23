# machine learning permite obter padrões e realizar predições
# através desses padrões


import tensorflow as tf

from processing.videoProcessing import *
from processing.processCsvFile import *
import os
import numpy as np
import librosa
import time

from numpy import argmax
from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


def convert_array_to_string(arr):
    string = ""
    for i in range(len(arr)):
        string += str(arr[i]) + ";"

    return string



def get_range_label(ini_idx, final_idx, video_number):
    # read the .csv file
    file = CsvFile("labeling/labeling_" + str(video_number) + ".csv", "r")

    # select intended columns from the file
    columns = file.get_columns(np.array([0, 3]))

    # iterate over the array and verify if its a ball hit
    for i in range(len(columns)):
        column = columns[i]
        first_sample = int(column[2])
        last_sample = int(column[3])

        condition_1 = column[0] == "racket" or column[0] == "floor" or \
                      column[0] == "glass" or column[0] == "grid" or \
                      column[0] == "net" or column[0] == "sel_warm_up"

        condition_2 = ini_idx >= first_sample and ini_idx <= last_sample
        condition_3 = final_idx >= first_sample and final_idx <= last_sample

        if condition_1 and (condition_2 or condition_3):
            return True

    return False


def organize_feature_values(f1, f2, f3, is_ball_hit):

    organized_arr = np.array([f1, f2, f3])
    organized_arr = np.ravel(organized_arr)
    organized_arr = np.append(organized_arr, [is_ball_hit * 1])

    return organized_arr


def generate_onset_array(arr, data_size, nog, spg):
    arr_size = data_size / spg # nr of onsets
    arr_size = int(arr_size) +1
    onset_array = np.zeros(arr_size)
    onset_array[arr] = 1

    return onset_array


def construct_3row_header_format(file, nr_of_features, nr_groups):
    nr_of_columns = nr_groups * nr_of_features +1

    # construct 1st header (f1, f2, f3, f4, f5, ...)
    idx_arr = np.arange(stop=nr_of_columns, dtype="int")
    idx_str_arr = np.array(idx_arr, dtype="str")
    f_str_arr = np.full(nr_of_columns, "f", dtype="str")
    first_header = np.char.add(f_str_arr, idx_str_arr)

    # construct 2nd header (d, c, d, d, d, c, c, ...)
    str_arr = np.empty(shape=nr_of_columns, dtype="str")
    str_arr[str_arr == ""] = "c"
    str_arr[-1] = "d"
    second_header = str_arr

    # construct 3rd header (, , , , ..., class)
    str_arr = list(np.empty(shape=nr_of_columns, dtype="str"))
    str_arr[-1] = "class"
    third_header = np.array(str_arr)

    file.write_one_line_on_file(first_header)
    file.write_one_line_on_file(second_header)
    file.write_one_line_on_file(third_header)

    return file


def get_features(data, nr_groups, nr_samples_per_group, nr_shifted_samples, sample_rate):
    # calculate features
    onset_feature = librosa.onset.onset_detect(y=data, sr=sample_rate, hop_length=nr_samples_per_group)
    onset_feature = generate_onset_array(onset_feature, len(data), nr_groups, nr_samples_per_group) # sets onsets indexes to 1 (where occured onset)
    rms_feature = librosa.feature.rms(y=data, hop_length=nr_samples_per_group)[0]
    specflux_feature = librosa.onset.onset_strength(y=data, sr=sample_rate, hop_length=nr_samples_per_group)

    # windowing the data
    onset_feature = tf.data.Dataset.from_tensor_slices(onset_feature)
    rms_feature = tf.data.Dataset.from_tensor_slices(rms_feature)
    specflux_feature = tf.data.Dataset.from_tensor_slices(specflux_feature)

    # nr_shifted_samples must be a multiple of nr_samples_per_group
    shift_nr = int(nr_shifted_samples/nr_samples_per_group)
    f1 = onset_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True)
    f2 = rms_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True)
    f3 = specflux_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True)

    f1 = f1.flat_map(lambda window: window.batch(nr_groups))
    f2 = f2.flat_map(lambda window: window.batch(nr_groups))
    f3 = f3.flat_map(lambda window: window.batch(nr_groups))

    return f1, f2, f3


def get_data_features(data, vd_index, nr_groups, nr_samples_per_group, nr_shifted_samples, sample_rate):

    arr_features_labels = np.array([])

    # features
    f1, f2, f3 = get_features(data, nr_groups, nr_samples_per_group, nr_shifted_samples, sample_rate)
    f1 = np.array(list(f1.as_numpy_iterator()))
    f2 = np.array(list(f2.as_numpy_iterator()))
    f3 = np.array(list(f3.as_numpy_iterator()))

    for j in range(len(f1)):  # f1, f2 and f3 have the same shape

        # verify if it's ball hit
        ini_idx = j * nr_samples_per_group
        final_idx = j * nr_samples_per_group + (nr_groups*nr_samples_per_group)
        is_ball_hit = get_range_label(ini_idx, final_idx, vd_index)

        # organize features and label in an array
        feature_arr = organize_feature_values(f1[j], f2[j], f3[j], is_ball_hit)

        # keep the features data on array
        arr_features_labels = np.append(arr_features_labels, feature_arr)
        file_rows.append(feature_arr)



def clear_dir(path_dir):
    for f in os.listdir(path_dir):
        os.remove(os.path.join(path_dir, f))


def dataset_construction(rel_path_videos, nr_groups, nr_samples_per_group, nr_features, nr_shifted_samples, sample_rate=44100):

    files = np.array(list(os.listdir(rel_path_videos)))
    for i in range(len(files)):
        v = Video(rel_path_videos, files[i])
        video = v.get_file()
        vd_idx = int(files[i].split(".")[0].split("_")[1][0:])
        print("Processing data from video number ", vd_idx, "...")
        audio_path = "../audios/AUDIO_" + str(vd_idx) + ".wav"
        video.audio.write_audiofile(audio_path, fps=sample_rate)
        y, sr = librosa.load(audio_path)
        get_data_features(y, vd_idx, nr_groups, nr_samples_per_group,
                                                nr_shifted_samples,
                                                sample_rate)

        features_file_train.write_lines_on_file(file_rows)


def separator(str):
    print("==============================================================================================================")
    print("                     ", str)
    print("==============================================================================================================")

# ================================================================

#                        TESTES

# ================================================================
start = time.time()
print("The program is running...")

# hyper-parameters
nog = 15  # number of groups
spr = 256  # samples per group
nof = 3  # number of features
noss = 1024  # number of sifted samples

separator("Defining the files for ODM")
file_rows = list()
features_file_train = CsvFile("processing/features_file_train.csv", "w")
features_file_train.write_lines_on_file([[""]])
features_file_train.clear_file()
#features_file_train = construct_3row_header_format(file=features_file_train,
#                                             nr_of_features=nof,
#                                             nr_groups=nog)

separator("Dataset Construction to train the model")
train = True
rel_path_train_videos = "../videos/train"
dataset_construction(rel_path_train_videos, nog, spr, nof, noss)


dataset = read_csv("features_file_train.csv", header=None)
X, y = dataset.values[:, :-1], dataset.values[:, -1]
X = X.astype('float32')
# encode strings to integer
y = LabelEncoder().fit_transform(y)
# split into train and test datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
# determine the number of input features
n_features = X_train.shape[1]
print("Number of features", n_features)

# define model
model = tf.keras.models.Sequential()
model.add(tf.keras.layers.Dense(10, activation='relu', kernel_initializer='he_normal', input_shape=(nof*nog,)))
model.add(tf.keras.layers.Dense(8, activation='relu', kernel_initializer='he_normal'))
model.add(tf.keras.layers.Dense(3, activation='softmax'))
model.add(tf.keras.layers.Dense(1))

model.summary()

# compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
# model.compile(loss="mse", optimizer=tf.keras.optimizers.SGD(learning_rate=1e-6, momentum=0.9))

# fit the model
model.fit(X_train, y_train, epochs=200, batch_size=32, verbose=2)
# evaluate the model
loss, acc = model.evaluate(X_test, y_test, verbose=2)

print("...................................................................")
print('Test Accuracy: %.3f' % acc)
print("Nr. of groups: ", nog)
print("Nr. of samples per group: ", spr)
print("Nr. of features: ", nof)
print("Nr. of shifted samples:", noss)


print("...................................................................")

file_rows = list()
features_file_train = CsvFile("processing/features_file_train.csv", "w")
features_file_train.write_lines_on_file([[""]])
features_file_train.clear_file()

separator("Dataset Construction to test the model")
rel_path_train_videos = "../videos/test"
dataset_construction(rel_path_train_videos, nog, spr, nof, noss)


dataset2 = read_csv("features_file_train.csv", header=None)
X, y = dataset2.values[:, :-1], dataset2.values[:, -1]
X = X.astype('float32')
# encode strings to integer
y = LabelEncoder().fit_transform(y)
# determine the number of input features
n_features = X_train.shape[1]
print("Number of features", n_features)

loss, acc = model.evaluate(X, y, verbose=0)

print("...................................................................")
print('Test Accuracy: %.3f' % acc)
print("Nr. of groups: ", nog)
print("Nr. of samples per group: ", spr)
print("Nr. of features: ", nof)
print("Nr. of shifted samples:", noss)

end = time.time()
print("Processing time: ", (end - start)/60, "minutes")


