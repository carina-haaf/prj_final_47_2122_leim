
import librosa
import tensorflow as tf
import numpy as np




def generate_onset_array(arr, data_size, nog, spg):

    arr_size = data_size / spg # nr of onsets
    arr_size = int(arr_size) +1
    onset_array = np.zeros(arr_size)
    onset_array[arr] = 1

    return onset_array




nog = 21  # number of groups
spr = 1024  # samples per group
nof = 3  # number of features
noss = 1024  # number of sifted samples



audio_path = "../audios/dataset/classification/AUDIO_39.wav"
data, sample_rate = librosa.load(audio_path)
print("data.shape: ", data.shape)
# calculate features
onset_feature = librosa.onset.onset_detect(y=data, sr=sample_rate, hop_length=spr)
onset_feature = generate_onset_array(onset_feature, len(data), nog, spr) # sets onsets indexes to 1 (where occured onset)
rms_feature = librosa.feature.rms(y=data, hop_length=spr)[0]
specflux_feature = librosa.onset.onset_strength(y=data, sr=sample_rate, hop_length=spr)

print("onset_shape: ", onset_feature.shape, "   rms_shape: ", rms_feature.shape, "   specflux_shape: ", specflux_feature.shape)


# windowing the data
onset_feature = tf.data.Dataset.from_tensor_slices(onset_feature)
rms_feature = tf.data.Dataset.from_tensor_slices(rms_feature)
specflux_feature = tf.data.Dataset.from_tensor_slices(specflux_feature)
print("onset_length: ", len(onset_feature), "   rms_length: ", len(rms_feature), "   specflux_length: ", len(specflux_feature))

shift_nr = int(noss/spr)
f1 = onset_feature.window(size=nog, shift=shift_nr, drop_remainder=True) # deliza entre 1 e N - verificar
f2 = rms_feature.window(size=nog, shift=shift_nr, drop_remainder=True)
f3 = specflux_feature.window(size=nog, shift=shift_nr, drop_remainder=True)

f1 = f1.flat_map(lambda window: window.batch(nog))
f2 = f2.flat_map(lambda window: window.batch(nog))
f3 = f3.flat_map(lambda window: window.batch(nog))

f1 = np.array(list(f1.as_numpy_iterator()))
f2 = np.array(list(f2.as_numpy_iterator()))
f3 = np.array(list(f3.as_numpy_iterator()))

print("f1 final len", f1.shape)

index = 0
for j in range(len(f1)):  # f1, f2 and f3 have the same shape


    # verify if it's ball hit
    ini_idx = j * noss
    final_idx = j * noss + (nog*spr)

    if final_idx < data.shape[0]:
        print("index: ", index)
        print("ini_idx: ", ini_idx, "  final_idx: ", final_idx)# debug

    else:
        break

    index += 1
