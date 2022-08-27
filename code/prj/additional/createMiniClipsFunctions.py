from additional.videoProcessing import *


def get_millis(ms):
    while ms > 999:
        ms -= 1000

    ms_value = ms
    return ms_value


def fill(value_type, value):
    if value_type != "hh" and value_type != "mm" and \
            value_type != "ss" and value_type != "ms":
        print("Wrong value type on fill method from createMiniClipsFunctions.py file")

    string = "" + str(value)
    if (value_type == "hh" or value_type == "mm" or value_type == "ss") and len(string) < 2:
        string = "0" + str(value)
    elif value_type == "ms":
        while len(string) < 3:
            string = "0" + string
    return string


def get_time(sample):
    millis = int((sample * 1000) / 44100)
    ms = get_millis(millis)
    seconds = (millis/1000) % 60
    seconds = int(seconds)
    minutes = (millis/(1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis/(1000 * 60 * 60)) % 24
    hours = hours if hours > 1 else 0  # porque há valores na ordem dos 1e-6

    # print(hours, minutes, seconds, ms)

    hh = fill("hh", hours)
    mm = fill("mm", minutes)
    ss = fill("ss", seconds)
    millisec = fill("ms", ms)

    s = str(hh) + ":" + str(mm) + ":" + str(ss) + "." + str(millisec)

    return s


"""

nog = 22  # number of groups
spr = 1024  # samples per group
nof = 3  # number of features
noss = 1024  # number of sifted samples

j = 172

ini_idx = j * noss
final_idx = j * noss + (nog * spr)

ini = get_time(ini_idx)
final = get_time(final_idx)

print(ini_idx, final_idx, ini, final)
newclip = mp.VideoFileClip("../test_videos/padel_58.mp4").subclip(ini, final)
newclip.write_videofile("../test_videos/ewe.mp4")

"""
