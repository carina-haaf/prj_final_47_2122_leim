import os
import numpy as np
import librosa
import soundfile as sf


class Audio:
    def __init__(self, rel_path, file_name, sr):
        self.rel_path = rel_path + "/" + file_name
        self.abs_path = self.get_abs_path()
        #print("PATH TODO: " + self.rel_path)

        audioclip, sample_rate = librosa.load(self.rel_path, sr=sr)
        self.sample_rate = sample_rate
        self.y = audioclip

    def get_rel_path(self):
        return self.rel_path

    def get_abs_path(self):
        return os.path.abspath("../" + self.rel_path)

    def get_audio_data(self):
        return self.y

    def get_audio_info(self):
        return sf.info(self.rel_path)

    def get_sample_rate(self):
        return self.sample_rate

    def write_audio(self, rel_path, file_name, y, sample_rate=44100):
        sf.write(rel_path + "/" + file_name, y, sample_rate)






"""
TESTES...

# obter um video
video = Video("padel_2.mp4")
print(video.get_file())



# dividir um video em "pedaços"
video = Video("padel.mp4")
video.split_video(vd_idx_ini=33, debug=False)



# teste com a classe...
new_dir = "../audios/classified_audios"
rel_path_audios = "../audios/dataset/train"
file_name = "AUDIO_" + str(36) + ".wav"

audio = Audio(rel_path_audios, file_name, 44100)
y = audio.get_audio_data()
y = y[16275:36755] # obtenção de um pequeno excerto do audio

audio.write_audio(new_dir, "ewe.wav", y, sample_rate=44100)



"""









