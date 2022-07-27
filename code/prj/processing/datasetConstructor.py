

import librosa
import tensorflow as tf
import numpy as np

from processing.videoProcessing import *
from processing.processCsvFile import *

from pandas import read_csv
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder


from processing.directoryManipulator import *

"""

Methods to create the dataset

"""




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
                      column[0] == "net" or column[0] == "self_warm_up"

        condition_2 = ini_idx >= first_sample and ini_idx <= last_sample
        # condition_3 = final_idx >= first_sample and final_idx <= last_sample

        if condition_1 and condition_2:
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


def create_file(path):

    features_file = CsvFile(path, "w")
    # features_file.clear_file()
    # features_file.write_lines_on_file([[""]])

    return features_file


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


    shift_nr = int(nr_shifted_samples/nr_samples_per_group)
    f1 = onset_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True) # deliza entre 1 e N - verificar
    f2 = rms_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True)
    f3 = specflux_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True)

    f1 = f1.flat_map(lambda window: window.batch(nr_groups))
    f2 = f2.flat_map(lambda window: window.batch(nr_groups))
    f3 = f3.flat_map(lambda window: window.batch(nr_groups))

    return f1, f2, f3


def get_data_features(data, vd_index, nr_groups, nr_samples_per_group, nr_shifted_samples, file_rows, non_ball_hit_vd_idx, sample_rate):
    nr_ball_hits = 0
    nr_non_ball_hits = 0

    # features
    f1, f2, f3 = get_features(data, nr_groups, nr_samples_per_group, nr_shifted_samples, sample_rate)
    f1 = np.array(list(f1.as_numpy_iterator()))
    f2 = np.array(list(f2.as_numpy_iterator()))
    f3 = np.array(list(f3.as_numpy_iterator()))
    # print("Shape f1: ", len(f1), "Shape f2: ", len(f2), "Shape f3: ", len(f3)) # debug

    for j in range(len(f1)):  # f1, f2 and f3 have the same shape

        # verify if it's ball hit
        ini_idx = j * nr_shifted_samples
        final_idx = j * nr_shifted_samples + (nr_groups*nr_samples_per_group)
        is_ball_hit = get_range_label(ini_idx, final_idx, vd_index)
        # print("ini_idx: ", ini_idx, "  final_idx: ", final_idx) # debug

        # organize features and label in an array
        feature_arr = organize_feature_values(f1[j], f2[j], f3[j], is_ball_hit)

        # keep the features data on array


        if (is_ball_hit and vd_index not in non_ball_hit_vd_idx) or \
                ((not is_ball_hit) and vd_index in non_ball_hit_vd_idx):
            file_rows.append(feature_arr)

        if is_ball_hit and vd_index not in non_ball_hit_vd_idx:
            nr_ball_hits += 1

        elif (not is_ball_hit) and vd_index in non_ball_hit_vd_idx:
            nr_non_ball_hits += 1
    """
    # para efeitos de contagem de eventos (equilíbrio do dataset)
    print("VIDEO: ", vd_index)
    print("Nr. batidas de bolas:", nr_ball_hits)
    print("Nr. NÃO batidas de bolas:", nr_non_ball_hits)
    # print("len(arr_features_labels): ", len(arr_features_labels))
    
    """

    return nr_ball_hits, nr_non_ball_hits


def construct(paths, nr_groups, nr_samples_per_group,
                         nr_shifted_samples, features_file,
                         file_rows, sample_rate=44100):

    total_ball_hits = 0
    total_non_ball_hits = 0

    non_ball_hit_vd_idx = [35, 36, 37, 40, 47]

    files = np.array(list(os.listdir(paths[0])))
    for i in range(len(files)):
        v = Video(paths[0], files[i])
        video = v.get_file()
        vd_idx = int(files[i].split(".")[0].split("_")[1][0:])
        print("Processing data from video number ", vd_idx, "...")

        audio_path = paths[1] + "/" + "AUDIO_" + str(vd_idx) + ".wav"
        video.audio.write_audiofile(audio_path, fps=sample_rate)
        y, sr = librosa.load(audio_path, sr=None)
        #print("y.shape: ", y.shape)

        nr_ball_hits, nr_non_ball_hits = get_data_features(y, vd_idx, nr_groups, nr_samples_per_group,
                        nr_shifted_samples,file_rows, non_ball_hit_vd_idx, sample_rate)

        total_ball_hits += nr_ball_hits
        total_non_ball_hits += nr_non_ball_hits

    features_file.write_lines_on_file(file_rows)

    print("\n\nTotal ball hits: ", total_ball_hits)
    print("Total NON ball hits: ", total_non_ball_hits)


def get_features_and_label_values(dataset, debug=False):

    X, y = dataset.values[:, :-1], dataset.values[:, -1]
    X = X.astype('float32')
    # encode strings to integer
    y = LabelEncoder().fit_transform(y)
    if debug:
        print("X.shape: ", X.shape, "y.shape: ", y.shape)

    return X, y


def get_train_and_test_sets(dataset, testSize=0.33, debug=False):

    X,y = get_features_and_label_values(dataset, debug)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=testSize)

    if debug:
        print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

    return X_train, X_test, y_train, y_test

