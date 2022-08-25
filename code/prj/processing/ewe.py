
import librosa
import numpy as np
import  librosa.display
import matplotlib.pyplot as plt


def manipulate(data, noise_factor):
    noise = np.random.randn(len(data))
    augmented_data = data + noise_factor * noise
    # Cast back to same data type
    augmented_data = augmented_data.astype(type(data[0]))
    return augmented_data


audio_path = "../audios/AUDIO_0"  ".wav"
y, sr = librosa.load(audio_path, sr=None)
fig, ax = plt.subplots(nrows=2, sharex=True)

y2 = manipulate(y, 0.01)

librosa.display.waveshow(y, sr=sr, x_axis='s', ax=ax[0], label='Audio Signal')
ax[0].legend(loc="upper right")

librosa.display.waveshow(y2, sr=sr, x_axis='s', ax=ax[1], label='Augmented Audio Signal')
ax[1].legend(loc="upper right")

plt.show()

