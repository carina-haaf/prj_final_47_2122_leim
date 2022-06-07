
from processing.processCsvFile import *
from processing.audioProcessing import *
from processing.directoryManipulator import *


def get_range_label(ini_idx, final_idx, video_number):
    """
    :param ini_idx:
    :param final_idx:
    :param video_number:
    :return:
    """
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


def classify(X, model, debug=False):
    y_est=model.predict(X)
    return y_est



def write_classified_audios(audio_data, X, y, y_est, vd_index, nr_groups, nr_samples_per_group, nr_sifted_samples):
    dir = "../audios/classified_audios/"
    clear_dir(dir)
    audio = audio_data.get_audio_data()
    print(audio.shape)
    audio_index = 0
    for i in range(0, len(audio), nr_sifted_samples):

        ini_idx = i
        final_idx = i + nr_groups * nr_samples_per_group
        is_ball_hit = get_range_label(ini_idx, final_idx, vd_index)

        idx = int(i/nr_sifted_samples)

        if (y[idx] == 1 and y_est[idx] == 1 or (y[idx] == 0 and y_est[idx] == 0)):

            if y[idx] == 1:
                mini_audio = audio[ini_idx:final_idx]
                file_name = "true_positive_ball_hit" + str(audio_index) + ".wav"
                print(file_name)
                audio_data.write_audio(dir, file_name, mini_audio, sample_rate=44100)

                audio_index += 1
            else:
                mini_audio = audio[ini_idx:final_idx]
                file_name = "true_positive_none_ball_hit" + str(audio_index) + ".wav"
                print(file_name)
                audio_data.write_audio(dir, file_name, mini_audio, sample_rate=44100)

                audio_index += 1
        elif y [idx] == 1 and y_est[idx] == 0:
            mini_audio = audio[ini_idx:final_idx]
            file_name = "false_negative_" + str(audio_index) + ".wav"
            print(file_name)
            audio_data.write_audio(dir, file_name, mini_audio, sample_rate=44100)

            audio_index += 1

        elif y [idx] == 0 and y_est[idx] == 1:
            mini_audio = audio[ini_idx:final_idx]
            file_name = "false_positive_" + str(audio_index) + ".wav"
            print(file_name)
            audio_data.write_audio(dir, file_name, mini_audio, sample_rate=44100)

            audio_index += 1


        #   print("ini: ", ini_idx, "       fin: ", final_idx)

def get_classified_audios(paths, nr_groups, nr_samples_per_group, nr_sifted_samples, X, y, y_est):

    files = np.array(list(os.listdir(paths[0])))
    for i in range(len(files)):
        vd_idx = int(files[i].split(".")[0].split("_")[1][0:])
        file_name = "AUDIO_" + str(vd_idx) + ".wav"

        audio = Audio(paths[1], file_name, 44100)
        write_classified_audios(audio, X, y, y_est, vd_idx, nr_groups, nr_samples_per_group, nr_sifted_samples)

"""
nog = 20
spg = 1024
noss = 4096

counter = 0
for i in range(0, 1279782, noss):

    ini_idx = i
    final_idx = i + nog*spg
    print("ini: ", ini_idx, "   fin: ", final_idx)
    counter += 1
    print(counter)

"""
