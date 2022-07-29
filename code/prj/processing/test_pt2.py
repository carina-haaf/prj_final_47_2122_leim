
# =================================================================================
# imports...
# =================================================================================

from processing import dataClassifier
from processing import datasetConstructor

from pandas import read_csv
import numpy as np
import matplotlib.pyplot as plt

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

from sklearn.metrics import accuracy_score, precision_score, \
                            recall_score, f1_score

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

# =================================================================================
# Ccnstrução e compilação do modelo ...
# =================================================================================

model = Sequential()
model.add(Dense(30, input_dim=63, activation='relu'))
model.add(Dense(30, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# =================================================================================
# Compilação e treino do modelo ...
# =================================================================================
# mean_squared_error
# binary_crossentropy (# 1e-6, 1e-4, 1e-2)

model.compile(loss='binary_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

list_score_metric = \
  [
    (accuracy_score, {}),
    (precision_score, {"average":"weighted"}), #macro #micro #weighted
    (recall_score, {"average":"weighted"}), #macro #micro #weighted
    (f1_score, {"average":"weighted"}), #macro #micro #weighted
  ]

# define 10-fold cross validation test harness
k_folds = 5
seed = 42
tt_split_indexes = datasetConstructor.stratified_fold_split(k_folds, seed=None)

cvscores = []
index = 0
for train_index, test_index in tt_split_indexes.split(X, Y):

    X_train, y_train = X[train_index], Y[train_index]
    X_test, y_test = X[test_index], Y[test_index]

    print(model.summary())
    history = model.fit(X_train, y_train, epochs=100, batch_size=20, verbose=2)

    y_predict = np.round_(model.predict(X_test ), 0)

    print("Confusion Matrix: ")
    print(confusion_matrix(y_test, y_predict))  # order matters! (actual, predicted)

    print(classification_report(y_test, y_predict))

    scores = model.evaluate(X_test, y_test, verbose=0)
    print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
    cvscores.append(scores[1] * 100)

    index += 1
    plt.plot(history.history['accuracy'], label='Test fold nr.' + str(index))
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend()

print("%.2f%% (+/- %.2f%%)" % (np.mean(cvscores), np.std(cvscores)))
plt.show()


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
dif = (end - start)/60
print('Processing time: ', float("{0:.2f}".format(dif)))

