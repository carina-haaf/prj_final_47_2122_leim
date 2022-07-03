import librosa
import soundfile as sf
from processing.directoryManipulator import *


dir = "../audios/classified_audios"
clear_dir(dir)

vd_idx = 51
paths = ["../videos/classification", "../audios/dataset/classification"]
audio_path = paths[1] + "/" + "AUDIO_" + str(vd_idx) + ".wav"

path_filename = dir + "/" + "ewe.wav"
audio_samples, sr = librosa.load(audio_path, sr=None)
sf.write(path_filename, audio_samples[0:21504], sr)
print(len(audio_samples))
