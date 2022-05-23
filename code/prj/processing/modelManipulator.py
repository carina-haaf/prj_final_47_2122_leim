

import tensorflow as tf




"""
Methods to create, train and evaluate models

"""


def construct(nr_features, nr_groups, debug=False):

    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(10, activation='relu', kernel_initializer='he_normal',
                                    input_shape=(nr_features*nr_groups,)))
    model.add(tf.keras.layers.Dense(8, activation='relu', kernel_initializer='he_normal'))
    model.add(tf.keras.layers.Dense(3, activation='softmax'))
    model.add(tf.keras.layers.Dense(1))

    if debug:
        model.summary()

    return model


def train_model(model, dsTuple, nr_epochs, nr_batches, vrb=0):

    model.compile(optimizer='adam', loss='mean_squared_error', metrics=['accuracy'])
    model.fit(dsTuple[0], dsTuple[2], epochs=nr_epochs, batch_size=nr_batches, verbose=vrb)

    return model


def evaluate_model(model, dsTuple, vrb=0):
    loss, acc = model.evaluate(dsTuple[1], dsTuple[3], verbose=vrb)
    print('Test Accuracy: %.3f' % acc)


def evaluate_model_v2(model, dsTuple, vrb=0):
    loss, acc = model.evaluate(dsTuple[0], dsTuple[1], verbose=vrb)
    print("...................................................................")
    print('Test Accuracy: %.3f' % acc)


