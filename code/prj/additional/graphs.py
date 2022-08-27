"""
https://librosa.org/doc/main/generated/librosa.onset.onset_detect.html#librosa.onset.onset_detect

"""

import librosa
import numpy as np
import  librosa.display
import matplotlib.pyplot as plt

audio_path = "../audios/AUDIO_" + str(1) + ".wav"
y, sr = librosa.load(audio_path)


# ONSET STRENGTH (Spectral flux)
o_env = librosa.onset.onset_strength(y=y, sr=sr)

# ONSET DETECT
# Return an array of time values to match the time axis from a feature matrix.
times = librosa.times_like(o_env, sr=sr)
onset_frames = librosa.onset.onset_detect(onset_envelope=o_env, sr=sr)


# RMS
S, phase = librosa.magphase(librosa.stft(y))
rms = librosa.feature.rms(S=S)
times_rms = librosa.times_like(rms)

# GRAPHS
fig, ax = plt.subplots(nrows=3, sharex=True)


ax[0].plot(times, o_env, label='Onset strength', color='black', alpha=0.6)
ax[0].vlines(times[onset_frames], 0, o_env.max(), color='r', alpha=0.4,
           linestyle='--', label='Onsets')
ax[0].legend(loc="upper right")
ax[0].set_title('Audio Features')


ax[1].semilogy(times_rms, rms[0], label='RMS Energy', color="green")
ax[1].legend(loc="upper right")


librosa.display.waveshow(y, sr=sr, x_axis='s', ax=ax[2], label='Audio Signal')
ax[2].legend(loc="upper right")

plt.show()
