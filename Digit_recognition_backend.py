import keras
import tensorflow as tf
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import numpy
import random
import globals

# backend


# https://data-flair.training/blogs/python-deep-learning-project-handwritten-digit-recognition/


def get_formated_data():
    (input_train, labels_train), (input_test, labels_test) = mnist.load_data()
    input_train = input_train.reshape(input_train.shape[0], 28, 28, 1)
    input_test = input_test.reshape(input_test.shape[0], 28, 28, 1)

    labels_train = keras.utils.to_categorical(labels_train, globals.num_classes)
    labels_test = keras.utils.to_categorical(labels_test, globals.num_classes)
    input_train = input_train.astype("float32")
    input_test = input_test.astype("float32")

    input_train /= 255
    input_test /= 255

    return input_train, input_test, labels_train, labels_test


def create_model():
    model = Sequential()
    model.add(
        Conv2D(
            32, kernel_size=(3, 3), activation="relu", input_shape=globals.input_shape
        )
    )
    model.add(Conv2D(64, (3, 3), activation="relu"))
    # model.add(MaxPooling2D())
    model.add(MaxPooling2D((2, 2)))

    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(256, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(globals.num_classes, activation="softmax"))
    model.compile(
        loss=keras.losses.categorical_crossentropy,
        optimizer=tf.keras.optimizers.Adadelta(),
        metrics=["accuracy"],
    )

    return model


def train_model(model, input_train, labels_train):
    hist = model.fit(
        input_train,
        labels_train,
        batch_size=64,
        epochs=100,
        verbose=1,
        # validation_data=(input_test, labels_test),
    )
    model.save("mnist3.h5")
    return hist


def get_random_digit(input_test):
    """
    Returns a random digit from the test set
    """

    r = random.randrange(globals.input_shape[0])
    digit = input_test[r]
    return digit.T[0] * 255


model = keras.models.load_model("mnist2.h5")


def predict_digit(inputs):
    results = model.predict(inputs.reshape(globals.input_shape).T)
    return results[0]


def evaluate(input_test, labels_test):
    score = model.evaluate(input_test, labels_test, verbose=0)
    print("score", score)
