import os
import numpy as np
import librosa
import soundfile as sf


class Audio:
    def __init__(self, audio_path, sr):

        audioclip, sample_rate = librosa.load(audio_path, sr=None)

        self.sample_rate = sample_rate
        self.y = audioclip

    def get_audio_data(self):
        return self.y

    def get_sample_rate(self):
        return self.sample_rate

    def write_audio(self, audio_path, y, sample_rate=44100):
        sf.write(audio_path, y, sample_rate)






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









