
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

# =================================================================================
# Iniciar contagem de tempo de processamento ...
# =================================================================================

start = time.time()
print("The program is running...")

# =================================================================================
# Definição do dataset ...
# =================================================================================

dataset = read_csv("../dataset/" + MAIN_DATASET_PATH, header=None)
X, Y = modelManipulator.get_features_and_label_values(dataset, debug=True)

nr_models = 130
fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True)

model = Sequential()
model.add(Dense(16, input_shape=(NR_OF_INPUT_LAYER_NODES,), kernel_regularizer=l1_l2(l1=1e-6, l2=1e-2), activation='relu')) # , kernel_regularizer=l2(1e-3)
model.add(Dropout(0.6))
model.add(Dense(8, activation="relu"))
model.add(Dropout(0.4))
model.add(Dense(4, activation="relu"))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))

# =================================================================================
# Model compilation ...
# =================================================================================
model.compile(loss=LOSS_FUNCTION,
              optimizer=tf.optimizers.Adam(learning_rate=LR),
              metrics=['accuracy'])

print("\n\nModel Summary: ")
print(model.summary())
history = model.fit(X, Y, epochs=NR_EPOCHS, batch_size=BATCH_SIZE, verbose=2)

# save model
# nr_models = directoryManipulator.get_nr_of_files("../models/constructed_models/")
#model.save(TRAINED_MODELS_PATH + "/model_" + str(nr_models + 1))
model.save(TRAINED_MODELS_PATH + "/model_131")
nr_models += 1

print("\n\n# =================================================================================")
print("                         T R A I N I N G    R E S U L T S")
print("# =================================================================================")

best_training_score = max(history.history['accuracy'])
print("\n\nBest training score (model history): ", best_training_score)

# =================================================================================
# Display Graphs ...
# =================================================================================

ax[0].plot(history.history['accuracy'], label='Model nr.' + str(nr_models + 1))
ax[0].legend(loc="lower right")
ax[0].set_title('Models Accuracy')
ax[0].set_xlabel('Epoch')
ax[0].set_ylabel('Accuracy')

ax[1].plot(history.history['loss'], label='Model nr.' + str(nr_models + 1))
ax[1].legend(loc="upper right")
ax[1].set_title('Models Loss')
ax[1].set_xlabel('Epoch')
ax[1].set_ylabel('Loss')


nr_models = directoryManipulator.get_nr_of_files(TRAINED_MODELS_PATH + "/")
fig.savefig(TRAINED_MODELS_GRAPHS_PATH + '/models_' + str(nr_models - 4) + '_to_' + str(nr_models) + '.png')

plt.show()


# =================================================================================
# Terminar contagem de tempo de processamento ...
# =================================================================================

end = time.time()
#  dif = (end - start)/60
dif = end - start
print('\n\nProcessing time: ', np.round_(dif, 0), "seconds")
