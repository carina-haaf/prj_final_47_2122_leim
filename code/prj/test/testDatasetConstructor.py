

import librosa
import tensorflow as tf

from additional.videoProcessing import *
from additional.processCsvFile import *

from additional.directoryManipulator import *
from additional.constants import *


"""

Methods to create the dataset

"""


def get_range_label(ini_idx, fin_idx, video_number):

    # read the .csv file
    # file = CsvFile(LABELING_FILES_PATH + "/labeling_" + str(video_number) + ".csv", "r")
    file = CsvFile(LABELING_TEST_FILES_PATH + "/labeling_" + str(video_number) + ".csv", "r")

    # select intended columns from the file
    columns = file.get_columns(np.array([0, 3]))

    # iterate over the array and verify if its a ball hit
    for i in range(len(columns)):
        column = columns[i]
        first_sample = int(column[2])
        last_sample = int(column[3])

        condition_1 = column[0] == "racket"

        interval = last_sample - first_sample
        percentage = int(PERCENTAGE * interval)
        l_s = first_sample + percentage

        condition_2 = fin_idx >= first_sample and ini_idx <= last_sample

        if condition_1 and condition_2:
            return True

    return False


def organize_feature_values(f1, f2, f3, is_ball_hit):

    organized_arr = np.array([f1, f2, f3])
    #organized_arr = np.array([f2])
    organized_arr = np.ravel(organized_arr)
    organized_arr = np.append(organized_arr, [is_ball_hit * 1])

    return organized_arr


def generate_onset_array(arr, data_size, spg):

    arr_size = data_size / spg  # nr of onsets
    arr_size = int(arr_size) + 1
    onset_array = np.zeros(arr_size)
    onset_array[arr] = 1

    return onset_array


def get_features(data, nr_groups, nr_samples_per_group, nr_shifted_samples, sample_rate):

    # calculate features
    onset_feature = librosa.onset.onset_detect(y=data, sr=sample_rate, hop_length=nr_samples_per_group)
    onset_feature = generate_onset_array(onset_feature, len(data), nr_samples_per_group)  # sets onsets indexes to 1 (where occured onset)
    rms_feature = librosa.feature.rms(y=data, hop_length=nr_samples_per_group)[0]
    specflux_feature = librosa.onset.onset_strength(y=data, sr=sample_rate, hop_length=nr_samples_per_group)

    # windowing the data
    onset_feature = tf.data.Dataset.from_tensor_slices(onset_feature)
    rms_feature = tf.data.Dataset.from_tensor_slices(rms_feature)
    specflux_feature = tf.data.Dataset.from_tensor_slices(specflux_feature)

    shift_nr = int(nr_shifted_samples/nr_samples_per_group)
    f1 = onset_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True)
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

        file_rows.append(feature_arr)
        if is_ball_hit:
            nr_ball_hits += 1

        elif not is_ball_hit:
            nr_non_ball_hits += 1

        """
        # keep the features data on array
        if (is_ball_hit and vd_index not in non_ball_hit_vd_idx) or \
                ((not is_ball_hit) and vd_index in non_ball_hit_vd_idx):
            file_rows.append(feature_arr)

        # counter of ball and non ball hits
        if is_ball_hit and vd_index not in non_ball_hit_vd_idx:
            nr_ball_hits += 1

        elif (not is_ball_hit) and vd_index in non_ball_hit_vd_idx:
            nr_non_ball_hits += 1
        
        """

    return nr_ball_hits, nr_non_ball_hits


def construct(paths, nr_groups, nr_samples_per_group,
              nr_shifted_samples, features_file,
              file_rows, sample_rate=44100):

    total_ball_hits = 0
    total_non_ball_hits = 0

    # non_ball_hit_vd_idx = [35, 36, 37, 47, 52, 53, 54]  # to balance dataset
    non_ball_hit_vd_idx = []

    files = np.array(list(os.listdir(paths[0])))
    for i in range(len(files)):
        v = Video(paths[0], files[i])
        video = v.get_file()
        vd_idx = int(files[i].split(".")[0].split("_")[1][0:])
        print("Processing data from video number ", vd_idx, "...")

        audio_path = paths[1] + "/" + "AUDIO_" + str(vd_idx) + ".wav"
        video.audio.write_audiofile(audio_path, fps=sample_rate)
        y, sr = librosa.load(audio_path, sr=None)

        nr_ball_hits, nr_non_ball_hits = get_data_features(y, vd_idx, nr_groups, nr_samples_per_group,
                                                           nr_shifted_samples, file_rows, non_ball_hit_vd_idx, sample_rate)

        total_ball_hits += nr_ball_hits
        total_non_ball_hits += nr_non_ball_hits

        """
        y2 = manipulate(y, 0.01)  # data augmentation

        nr_ball_hits, nr_non_ball_hits = get_data_features(y2, vd_idx, nr_groups, nr_samples_per_group,
                                                           nr_shifted_samples, file_rows, non_ball_hit_vd_idx, sample_rate)

        total_ball_hits += nr_ball_hits
        total_non_ball_hits += nr_non_ball_hits
        """

    features_file.write_lines_on_file(file_rows)

    print("\n\nTotal ball hits: ", total_ball_hits)
    print("Total NON ball hits: ", total_non_ball_hits)


def manipulate(data, noise_factor):
    noise = np.random.randn(len(data))
    augmented_data = data + noise_factor * noise
    # Cast back to same data type
    augmented_data = augmented_data.astype(type(data[0]))
    return augmented_data
