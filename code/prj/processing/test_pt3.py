# teste parecido com o test_pt2.py, mas neste caso carrega um modelo já treinado
# =================================================================================
# imports...
# =================================================================================

from processing import datasetConstructor

from pandas import read_csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import classification_report

from keras.models import load_model

import os
import pickle

import time

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
k_folds = 6
tt_split_indexes = datasetConstructor.stratified_fold_split(k_folds, seed=None)

index = 1  # model index

fig, ax = plt.subplots(nrows=1, ncols=2, sharex=True)
for train_index, test_index in tt_split_indexes.split(X, Y):

    # Load model
    model = load_model('../models/constructed_models/model_' + str(index))
    model.summary()

    X_train, y_train = X[train_index], Y[train_index]
    X_test, y_test = X[test_index], Y[test_index]

    print("\n\nModel Summary: ")
    print(model.summary())

    y_predict = model.predict(X_test)
    y_predict = np.where(y_predict > 0.5, 1, 0)

    print("\n\n# =================================================================================")
    print("                         V A L I D A T I O N    R E S U L T S")
    print("# =================================================================================")

    print("\n\nConfusion Matrix: ")
    print(confusion_matrix(y_test, y_predict))  # order matters! (actual, predicted)

    print("\n\nClassification Report: ")
    print(classification_report(y_test, y_predict))

    loss, accuracy = model.evaluate(X_test, y_test, batch_size=33, verbose=0)

    print("\n\nEvaluation Matrics:")
    print("Accuracy: ", accuracy)
    print("Loss: ", loss)

    index += 1




"""
# =================================================================================
# Obtenção matriz de confusão para dados novos ...
# =================================================================================

print("\n\n\n=================================================================================")
print("\tConfusion matrix for test fold...")
print("=================================================================================")
print(confusion_matrix(y_class_true, y_class_est))# order matters! (actual, predicted)
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
print('Processing time: ', np.round_(dif, 0), "seconds")

