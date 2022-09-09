
# =================================================================================
# imports...
# =================================================================================

from model import modelManipulator
from additional import directoryManipulator
from additional.constants import *

import matplotlib.pyplot as plt
from pandas import read_csv
import numpy as np
import time

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

from keras.regularizers import l2, l1, l1_l2

import sklearn.preprocessing as pp
from sklearn.decomposition import PCA


from keras.layers import Dropout
import pickle

# =================================================================================
# Iniciar contagem de tempo de processamento ...
# =================================================================================

start = time.time()
print("The program is running...")

# =================================================================================
# Get dataset ...
# =================================================================================

dataset = read_csv("../dataset/" + MAIN_DATASET_PATH, header=None)
X_non_scaled, Y = modelManipulator.get_features_and_label_values(dataset, debug=True)

# nr_models = 130
fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True)

# =================================================================================
# Data pre-processing ...
# =================================================================================
scaler = pp.StandardScaler().fit(X_non_scaled)
X = scaler.transform(X_non_scaled)
pickle.dump(scaler, open(TRAINED_MODELS_WITH_ALL_DATA_PATH + "/scaler_" + str(EXPERIMENT) + ".pkl", 'wb'))


# =================================================================================
# Model construction ...
# =================================================================================



model = Sequential()
model.add(Dense(64, input_shape=(NR_OF_INPUT_LAYER_NODES,),
			activation=HIDDEN_LAYERS_ACTIVATION_FUNCTION))

model.add(Dropout(0.4))

model.add(Dense(1, activation=OUTPUT_ACTIVATION_FUNCTION))


# =================================================================================
# Model compilation ...
# =================================================================================
model.compile(loss=LOSS_FUNCTION,
              optimizer=tf.optimizers.Adam(learning_rate=LR),
              metrics=['accuracy'])

print("\n\nModel Summary: ")
print(model.summary())
history = model.fit(X, Y, epochs=NR_EPOCHS, batch_size=BATCH_SIZE, verbose=2)


# =================================================================================
# Save model ...
# =================================================================================

# nr_models = directoryManipulator.get_nr_of_files("../models/constructed_models/")
model_nr = EXPERIMENT
model.save(TRAINED_MODELS_WITH_ALL_DATA_PATH + "/trained_model_" + str(model_nr))

print("\n\n# =================================================================================")
print("                         T R A I N I N G    R E S U L T S")
print("# =================================================================================")

best_training_score = max(history.history['accuracy'])
print("\n\nBest training score (model history): ", best_training_score)

# =================================================================================
# Display Graphs ...
# =================================================================================

ax[0].plot(history.history['accuracy'], label='Model nr.' + str(model_nr))
ax[0].legend(loc="lower right")
ax[0].set_title('Model Accuracy')
ax[0].set_xlabel('Epoch')
ax[0].set_ylabel('Accuracy')

ax[1].plot(history.history['loss'], label='Model nr.' + str(model_nr))
ax[1].legend(loc="upper right")
ax[1].set_title('Model Loss')
ax[1].set_xlabel('Epoch')
ax[1].set_ylabel('Loss')


# nr_models = directoryManipulator.get_nr_of_files(TRAINED_MODELS_PATH + "/")
# fig.savefig(TRAINED_MODELS_GRAPHS_PATH + '/models_' + str(nr_models - 4) + '_to_' + str(nr_models) + '.png')

plt.show()


# =================================================================================
# Terminar contagem de tempo de processamento ...
# =================================================================================

end = time.time()
#  dif = (end - start)/60
dif = end - start
print('\n\nProcessing time: ', np.round_(dif, 0), "seconds")
