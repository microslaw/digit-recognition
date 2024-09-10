import keras
from keras.datasets import mnist
import random
import globals
import numpy as np


# backend
model = keras.models.load_model("models\mnist2.h5")


# https://data-flair.training/blogs/python-deep-learning-project-handwritten-digit-recognition/


def get_formated_data():
    (input_train, labels_train), (input_test, labels_test) = mnist.load_data()
    print(input_train.shape)
    input_train = input_train.reshape(input_train.shape[0], 28, 28, 1)
    input_test = input_test.reshape(input_test.shape[0], 28, 28, 1)

    labels_train = keras.utils.to_categorical(labels_train, globals.num_classes)
    labels_test = keras.utils.to_categorical(labels_test, globals.num_classes)
    input_train = input_train.astype("float32")
    input_test = input_test.astype("float32")

    input_train /= 255
    input_test /= 255

    # shuffling the data
    input = np.concatenate((input_test, input_train), axis=0)
    labels = np.concatenate((labels_test, labels_train), axis=0)

    samples = input.shape[0]
    test_train_ratio = 1 / 7

    train_idxs = np.random.choice(
        np.arange(samples),
        int(samples * test_train_ratio),
        replace=False,
    )
    test_idxs = np.setdiff1d(np.arange(samples), train_idxs).shape

    input_train = input.take(train_idxs, axis=0)
    input_test = input.take(test_idxs, axis=0)
    labels_train = labels.take(train_idxs, axis=0)
    labels_test = labels.take(test_idxs, axis=0)

    return input_train, input_test, labels_train, labels_test


def get_random_digit(input_test):
    """
    Returns a random digit from the test set
    """

    r = random.randrange(globals.input_shape[0])
    digit = input_test[r]
    return digit.T[0] * 255


def predict_digit(inputs):
    results = model.predict(inputs.reshape(globals.input_shape).T)
    return results[0]
