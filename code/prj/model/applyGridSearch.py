
# =================================================================================
# imports...
# =================================================================================

from processing import datasetConstructor

from pandas import read_csv
import numpy as np
import time

from sklearn.model_selection import GridSearchCV

from sklearn.model_selection import StratifiedKFold
from scikeras.wrappers import KerasClassifier

from keras.models import Sequential
from keras.layers import Dense



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

model = Sequential()
model.add(Dense(34, input_dim=66, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

"""
model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
"""

model = KerasClassifier(model=model, verbose=2, loss='binary_crossentropy', metrics=['accuracy'])
# define the grid search parameters
batch_size = [1, 5, 10]
optimizer = ['SGD', 'Adam']
learn_rate = [0.0001, 0.001, 0.01]
epochs=[200]
param_grid = dict(epochs=epochs, batch_size=batch_size, optimizer=optimizer, optimizer__learning_rate=learn_rate)
grid = GridSearchCV(estimator=model, param_grid=param_grid, n_jobs=-1, cv=StratifiedKFold( n_splits=5,
                                      shuffle=True, random_state=None ), verbose=4)
grid_result = grid.fit(X, Y)
# summarize results
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
means = grid_result.cv_results_['mean_test_score']
stds = grid_result.cv_results_['std_test_score']
params = grid_result.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))


# =================================================================================
# Terminar contagem de tempo de processamento ...
# =================================================================================
end = time.time()
#  dif = (end - start)/60
dif = end - start
print('Processing time: ', np.round_(dif, 0), "seconds")
