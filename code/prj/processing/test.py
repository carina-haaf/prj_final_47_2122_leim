import librosa


arr = []




onset_feature = librosa.onset.onset_detect(y=data, sr=sample_rate, hop_length=nr_samples_per_group)
onset_feature = generate_onset_array(onset_feature, len(data), nr_groups, nr_samples_per_group) # sets onsets indexes to 1 (where occured onset)
rms_feature = librosa.feature.rms(y=data, hop_length=nr_samples_per_group)[0]
specflux_feature = librosa.onset.onset_strength(y=data, sr=sample_rate, hop_length=nr_samples_per_group)

# windowing the data
onset_feature = tf.data.Dataset.from_tensor_slices(onset_feature)

# nr_shifted_samples must be a multiple of nr_samples_per_group
shift_nr = int(nr_shifted_samples/nr_samples_per_group)
f1 = onset_feature.window(size=nr_groups, shift=shift_nr, drop_remainder=True)

f1 = f1.flat_map(lambda window: window.batch(nr_groups))
