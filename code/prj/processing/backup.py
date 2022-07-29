# BACKUP test_pt2.py
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

import time


# =================================================================================
# Iniciar contagem de tempo de processamento ...
# =================================================================================

start = time.time()
print("The program is running...")

# =================================================================================
# Definição dos datasets de treino e teste ...
# =================================================================================

dataset = read_csv("features_file.csv", header=None)
X, Y = datasetConstructor.get_features_and_label_values(dataset, debug=True)

# =================================================================================
# Definição/ ccnstrução do modelo ...
# =================================================================================

model = Sequential()
model.add(Dense(30, input_dim=63, activation='relu'))
model.add(Dense(30, activation='relu'))
model.add(Dense(1, activation='sigmoid'))


# =================================================================================
# Compilação e treino do modelo ...
# =================================================================================
# mean_squared_error
# binary_crossentropy
# 1e-6, 1e-4, 1e-2
model.compile(loss='binary_crossentropy',
              optimizer=tf.keras.optimizers.SGD(lr=1e-6, momentum=0.9),
              metrics=['accuracy'])
history = model.fit(X, Y, epochs=100, batch_size=20, verbose=2)
plt.plot(history.history['accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.show()

"""
# =================================================================================
# Valores obtidos após classes estimadas ...
# =================================================================================



print("\n\n\n=================================================================================")
print("\tEstimated classes values FOR NEW DATA...")
print("=================================================================================")

y_class_est = np.round_(model.predict(X_class), 0)

print("'y_class_true' unique values: ", np.unique(y_class_true), "   len(y_class_true): ", len(y_class_true))
print("'y_class_est' unique values: ", np.unique(y_class_est), "   len(y_class_est): ", len(y_class_est))



# =================================================================================
# Obtenção matriz de confusão para dados novos ...
# =================================================================================

print("\n\n\n=================================================================================")
print("\tConfusion matrix for new data...")
print("=================================================================================")
print(confusion_matrix(y_class_true, y_class_est))# order matters! (actual, predicted)
#       o   1
#  ô  [TN, FP]
#  î  [FN, TP]


# =================================================================================
# Resumo da classificação ...
# =================================================================================

print("\n\n\n=================================================================================")
print("\tClassification Report ...")
print("=================================================================================")

print(classification_report(y_class_true, y_class_est))


print("\n\n\n=================================================================================")
print("\tModel Evaluation ...")
print("=================================================================================")
print("Evaluate Model:\n", model.evaluate(X_class, y_class_true))


# =================================================================================
# Criar ficheiros .wav com os resultados da classificação sobre novos dados ...
# =================================================================================

print("\n\n\n=================================================================================")
print("\tWrite audios with results ...")
print("=================================================================================")

nog = 21  # number of groups
spr = 1024  # samples per group
nof = 3  # number of features
noss = 2048  # number of sifted samples

paths_classification = ["../videos/classification", "../audios/dataset/classification"]
dataClassifier.get_classified_audios(paths_classification, nog, spr, noss, y_class_true, y_class_est)

# =================================================================================
# Terminar contagem de tempo de processamento ...
# =================================================================================

end = time.time()
dif = (end - start)/60
print('Processing time: ', float("{0:.2f}".format(dif)))
"""
