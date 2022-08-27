

import tensorflow as tf

from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

"""
Methods to create, train and evaluate models

"""


def construct(nr_features, nr_groups, debug=False):
    """
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(10, activation='relu', kernel_initializer='he_normal',
                                    input_shape=(nr_features*nr_groups,)))
    model.add(tf.keras.layers.Dense(8, activation='relu', kernel_initializer='he_normal'))
    model.add(tf.keras.layers.Dense(3, activation='relu'))
    model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    """

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(30, input_dim=nr_features*nr_groups, activation='relu'))
    model.add(tf.keras.layers.Dense(30, activation='relu'))
    model.add(tf.keras.layers.Dense(1))

    if debug:
        model.summary()

    return model


def train_model(model, ds_tuple, nr_epochs, nr_batches, vrb=0):

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
    model.fit(ds_tuple[0], ds_tuple[2], epochs=nr_epochs, batch_size=nr_batches, verbose=vrb)

    return model


def evaluate_model(model, ds_tuple, vrb=0):
    loss, acc = model.evaluate(ds_tuple[1], ds_tuple[3], verbose=vrb)
    print('Test Accuracy: %.3f' % acc)


def evaluate_model_v2(model, dsTuple, vrb=0):
    loss, acc = model.evaluate(dsTuple[0], dsTuple[1], verbose=vrb)
    print("...................................................................")
    print('Test Accuracy: %.3f' % acc)


def stratified_fold_split(k_folds, seed=None):
    # yields indices to random split of data into:
    # - k consecutive folds (k_folds parameter)
    # - each fold used once as validation; the k-1 remaining folds as training dataset
    # - shuffle=True, so dataset is shuffled (random split) before building the folds
    # - datasets preserve the percentage of samples for each class
    tt_split_indexes = StratifiedKFold(n_splits=k_folds,
                                       shuffle=True, random_state=seed)
    return tt_split_indexes


def get_features_and_label_values(dataset, debug=False):

    x, y = dataset.values[:, :-1], dataset.values[:, -1]
    x = x.astype('float32')
    # encode strings to integer
    y = LabelEncoder().fit_transform(y)
    if debug:
        print("X.shape: ", x.shape, "y.shape: ", y.shape)

    return x, y


def get_train_and_test_sets(dataset, test_size=0.33, debug=False):

    x, y = get_features_and_label_values(dataset, debug)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=test_size)

    if debug:
        print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)

    return x_train, x_test, y_train, y_test
