
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
import pickle


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


# =================================================================================
# Training ...
# =================================================================================
# define k-fold cross validation test harness
k_folds = NR_KFOLDS
tt_split_indexes = modelManipulator.stratified_fold_split(k_folds)

train_scores = []
train_losses = []

validation_scores = []
validation_losses = []

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True)
nr_models = 0
for train_index, test_index in tt_split_indexes.split(X, Y):

    # =================================================================================
    # Model construction ...
    # =================================================================================
    # kernel_regularizer=l2(1e-3), kernel_regularizer=l1_l2(l1=1e-3, l2=1e-3),

    model = Sequential()
    model.add(Dense(256, input_shape=(NR_OF_INPUT_LAYER_NODES,),
                    kernel_regularizer=l2(l2=1e-5),
                    activation=HIDDEN_LAYERS_ACTIVATION_FUNCTION))

    model.add(Dropout(0.45))

    model.add(Dense(1, activation=OUTPUT_ACTIVATION_FUNCTION))



    # =================================================================================
    # Model compilation ...
    # =================================================================================
    model.compile(loss=LOSS_FUNCTION,
                  optimizer=tf.optimizers.Adam(learning_rate=LR),
                  metrics=['accuracy'])

    # =================================================================================
    # Data pre-processing ...
    # =================================================================================
    X_train, y_train = X[train_index], Y[train_index]
    X_test, y_test = X[test_index], Y[test_index]

    scaler = pp.StandardScaler().fit(X_train)
    x_train = scaler.transform(X_train)

    # save scaler
    pickle.dump(scaler, open(TRAINED_MODELS_PATH + "/scaler_" + str(nr_models + 1) + ".pkl", 'wb'))

    x_test = scaler.transform(X_test)

    # =================================================================================
    # Train model  ...
    # =================================================================================

    print("\n\nModel Summary: ")
    print(model.summary())
    history = model.fit(x_train, y_train, epochs=NR_EPOCHS, batch_size=BATCH_SIZE, verbose=2)

    # =================================================================================
    # Save model  ...
    # =================================================================================
    model.save(TRAINED_MODELS_PATH + "/model_" + str(nr_models + 1))
    nr_models += 1

    y_predict = model.predict(x_test)
    y_predict = np.where(y_predict > DECISION_LIMIT, 1, 0)

    print("\n\n# =================================================================================")
    print("                         T R A I N I N G    R E S U L T S")
    print("# =================================================================================")

    best_training_score = max(history.history['accuracy'])
    minimum_loss = min(history.history['loss'])

    train_scores.append(best_training_score * 100)
    train_losses.append(minimum_loss * 100)

    print("\n\nBest training score (model history): ", best_training_score)
    print("Minimum loss (model history): ", minimum_loss)

    print("\n\n# =================================================================================")
    print("                         V A L I D A T I O N    R E S U L T S")
    print("# =================================================================================")

    print("\n\nConfusion Matrix: ")
    print(confusion_matrix(y_test, y_predict))  # order matters! (actual, predicted)

    print("\n\nClassification Report: ")
    print(classification_report(y_test, y_predict, target_names=("noise", "hit")))

    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)

    validation_scores.append(accuracy * 100)
    validation_losses.append(loss * 100)

    print("\n\nEvaluation Matrics:")
    print("Accuracy: ", accuracy)
    print("Loss: ", loss)

    # =================================================================================
    # Display Graphs ...
    # =================================================================================

    ax[0].plot(history.history['accuracy'], label='Model nr.' + str(nr_models))
    ax[0].legend(loc="lower right")
    ax[0].set_title('Models Accuracy')
    ax[0].set_xlabel('Epoch')
    ax[0].set_ylabel('Accuracy')

    ax[1].plot(history.history['loss'], label='Model nr.' + str(nr_models))
    ax[1].legend(loc="upper right")
    ax[1].set_title('Models Loss')
    ax[1].set_xlabel('Epoch')
    ax[1].set_ylabel('Loss')


nr_models = directoryManipulator.get_nr_of_files(TRAINED_MODELS_PATH + "/")
fig.savefig(TRAINED_MODELS_GRAPHS_PATH + '/models_' + str(nr_models - 4) + '_to_' + str(nr_models) + '.png')

print("\n\nAverage train accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(train_scores), np.std(train_scores)))
print("Average train loss: %.2f%% (+/- %.2f%%)" % (np.mean(train_losses), np.std(train_losses)))

print("\n\nAverage validation accuracy: %.2f%% (+/- %.2f%%)" % (np.mean(validation_scores), np.std(validation_scores)))
print("Average validation loss: %.2f%% (+/- %.2f%%)" % (np.mean(validation_losses), np.std(validation_losses)))

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
