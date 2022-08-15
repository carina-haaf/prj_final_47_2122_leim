
# =================================================================================
# imports...
# =================================================================================

from processing import datasetConstructor
from processing import directoryManipulator

import matplotlib.pyplot as plt
from pandas import read_csv
import numpy as np
import time
import os

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

from keras.models import Sequential
from keras.layers import Dense

import tensorflow as tf


# =================================================================================
# Iniciar contagem de tempo de processamento ...
# =================================================================================

start = time.time()
print("The program is running...")

# =================================================================================
# Definição do dataset ...
# =================================================================================

dataset = read_csv("features_file.csv", header=None)
X, Y = datasetConstructor.get_features_and_label_values(dataset, debug=True)


# define k-fold cross validation test harness
k_folds = 5
tt_split_indexes = datasetConstructor.stratified_fold_split(k_folds, seed=None)

cvscores = []
losses = []
nr_models = -1

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True)
for train_index, test_index in tt_split_indexes.split(X, Y):

    # =================================================================================
    # Model construction ...
    # =================================================================================

    model = Sequential()
    model.add(Dense(35, input_dim=66, activation='relu'))
    #model.add(Dense(18, activation='relu'))
    model.add(Dense(1, activation='sigmoid'))

    # =================================================================================
    # Model compilation ...
    # =================================================================================

    model.compile(loss='binary_crossentropy',
                  optimizer=tf.keras.optimizers.Adam(learning_rate=0.1),
                  metrics=['accuracy'])

    X_train, y_train = X[train_index], Y[train_index]
    X_test, y_test = X[test_index], Y[test_index]

    print("\n\nModel Summary: ")
    print(model.summary())
    history = model.fit(X_train, y_train, epochs=200, batch_size=512, verbose=2)

    # save model
    nr_models = directoryManipulator.get_nr_of_files("../models/constructed_models/")
    model.save("../models/constructed_models/model_" + str(nr_models + 1))

    y_predict = model.predict(X_test)
    y_predict = np.where(y_predict > 0.5, 1, 0)

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
    print(classification_report(y_test, y_predict))

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


nr_models = directoryManipulator.get_nr_of_files("../models/constructed_models/")
fig.savefig('../models/models_graphs/models_' + str(nr_models - 4) + '_to_' + str(nr_models) + '.png')
print("\n\nAverage accuracy:%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
print("Average accuracy:%.2f%% (+/- %.2f%%)" % (np.mean(losses), np.std(losses)))
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

