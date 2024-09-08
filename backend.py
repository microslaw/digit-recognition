import keras
from keras.datasets import mnist
import random
import globals

# backend
model = keras.models.load_model("mnist2.h5")


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
