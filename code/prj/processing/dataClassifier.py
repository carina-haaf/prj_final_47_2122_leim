
from processing.processCsvFile import *
from processing.audioProcessing import *
from processing.directoryManipulator import *
import soundfile as sf

from scipy.io.wavfile import read, write


def get_range_label(ini_idx, final_idx, video_number):
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


def write_classified_audios(audio_samples, y_true_class, y_est_class, nr_groups, nr_samples_per_group, nr_sifted_samples, vd_index):
    dir = "../audios/classified_audios"
    clear_dir(dir)

    audio_index = 0
    file_name = ""

    for i in range(0, len(audio_samples), nr_sifted_samples):

        ini_idx = i
        final_idx = i + nr_groups * nr_samples_per_group

        if final_idx < len(audio_samples):
            idx = int(i / nr_sifted_samples)

            if y_est_class[idx] == 1 and y_true_class[idx] == 1:
                file_name = "VD_" + str(vd_index) +"_TP_" + str(ini_idx) + "_" + str(final_idx) + ".wav"

            elif y_est_class[idx] == 0 and y_true_class[idx] == 0:
                file_name = "VD_" + str(vd_index) +"_TN_" + str(ini_idx) + "_" + str(final_idx) + ".wav"

            elif y_est_class[idx] == 0 and y_true_class[idx] == 1:
                file_name = "VD_" + str(vd_index) +"_FN_" + str(ini_idx) + "_" + str(final_idx) + ".wav"

            elif y_est_class[idx] == 1 and y_true_class[idx] == 0:
                file_name = "VD_" + str(vd_index) +"_FP_" + str(ini_idx) + "_" + str(final_idx) + ".wav"
        
            mini_audio = audio_samples[ini_idx : final_idx]


            path_filename = dir + "/" + file_name
            write(path_filename, 44100, mini_audio)

            # sf.write(path_filename, mini_audio, 44100)
            audio_index += 1

        #print(file_name) # debug
        #print("ini: ", ini_idx, "       fin: ", final_idx) #debug


def get_classified_audios(paths, nr_groups, nr_samples_per_group, nr_sifted_samples, y_true_class, y_est_class):

    files = np.array(list(os.listdir(paths[0])))
    for i in range(len(files)):
        vd_idx = int(files[i].split(".")[0].split("_")[1][0:])
        #file_name = "AUDIO_" + str(vd_idx) + ".wav"
        audio_path = paths[1] + "/" + "AUDIO_" + str(vd_idx) + ".wav"

        audio_samples, sr = librosa.load(audio_path, sr=None)
        write_classified_audios(audio_samples, y_true_class, y_est_class, nr_groups, nr_samples_per_group, nr_sifted_samples, vd_idx)

    print("Audio chunks created successfully.\n\n")


