
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

# define k-fold cross validation test harness
k_folds = 5
tt_split_indexes = modelManipulator.stratified_fold_split(k_folds, seed=42)

cvscores = []
losses = []

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True)
nr_models = 130
for train_index, test_index in tt_split_indexes.split(X, Y):

    # =================================================================================
    # Model construction ...
    # =================================================================================

    model = Sequential()
    model.add(Dense(32, input_shape=(NR_OF_INPUT_LAYER_NODES,), kernel_regularizer=l1_l2(l1=1e-3, l2=1e-3), activation='relu')) # , kernel_regularizer=l2(1e-3)
    model.add(Dropout(0.4))
    #model.add(Dense(64, activation="relu"))
    #model.add(Dropout(0.2))
    model.add(Dense(1, activation='sigmoid'))

    # =================================================================================
    # Model compilation ...
    # =================================================================================
    model.compile(loss=LOSS_FUNCTION,
                  optimizer=tf.optimizers.Adam(learning_rate=LR),
                  metrics=['accuracy'])

    X_train, y_train = X[train_index], Y[train_index]
    X_test, y_test = X[test_index], Y[test_index]

    #X_train = pp.normalize(X_train)
    #X_test = pp.normalize(X_test)

    print("\n\nModel Summary: ")
    print(model.summary())
    history = model.fit(X_train, y_train, epochs=NR_EPOCHS, batch_size=BATCH_SIZE, verbose=2)

    # save model
    # nr_models = directoryManipulator.get_nr_of_files("../models/constructed_models/")
    model.save(TRAINED_MODELS_PATH + "/model_" + str(nr_models + 1))
    nr_models += 1

    y_predict = model.predict(X_test)
    y_predict = np.where(y_predict > DECISION_LIMIT, 1, 0)

    print("\n\n# =================================================================================")
    print("                         T R A I N I N G    R E S U L T S")
    print("# =================================================================================")

    best_training_score = max(history.history['accuracy'])
    print("\n\nBest training score (model history): ", best_training_score)

    print("\n\n# =================================================================================")
    print("                         V A L I D A T I O N    R E S U L T S")
    print("# =================================================================================")

    print("\n\nConfusion Matrix: ")
    print(confusion_matrix(y_test, y_predict))  # order matters! (actual, predicted)

    print("\n\nClassification Report: ")
    print(classification_report(y_test, y_predict, target_names=("noise", "hit")))

    loss, accuracy = model.evaluate(X_test, y_test, verbose=0)

    cvscores.append(accuracy * 100)
    losses.append(loss * 100)

    print("\n\nEvaluation Matrics:")
    print("Accuracy: ", accuracy)
    print("Loss: ", loss)

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
print("\n\nAverage accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
print("Average loss: %.2f%% (+/- %.2f%%)" % (np.mean(losses), np.std(losses)))
plt.show()


"""
#       o   1
#  ô  [TN, FP]
#  î  [FN, TP]
"""


# =================================================================================
# Terminar contagem de tempo de processamento ...
# =================================================================================

end = time.time()
#  dif = (end - start)/60
dif = end - start
print('\n\nProcessing time: ', np.round_(dif, 0), "seconds")
