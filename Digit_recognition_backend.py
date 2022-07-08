import keras 
import tensorflow as tf
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D
import numpy
from keras.utils import np_utils
import random

#backend



#https://data-flair.training/blogs/python-deep-learning-project-handwritten-digit-recognition/

def format_data():
    global num_classes
    num_classes = 10
    global input_train
    global input_test
    global labels_test
    global labels_train
    global input_shape
    (input_train, labels_train), (input_test,labels_test) = mnist.load_data()
    input_shape = (28, 28, 1)
    input_train = input_train.reshape(input_train.shape[0],28,28,1)
    input_test = input_test.reshape(input_test.shape[0],28,28,1)

    labels_train = keras.utils.np_utils.to_categorical(labels_train, num_classes)
    labels_test= keras.utils.np_utils.to_categorical(labels_test, num_classes)

    input_train = input_train.astype('float32')
    input_test = input_test.astype('float32')

    input_train /=255
    input_test /=255


def make_model():
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),activation='relu',input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation='relu'))
    #model.add(MaxPooling2D())
    model.add(MaxPooling2D((2, 2)))

    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(256, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))
    model.compile(loss=keras.losses.categorical_crossentropy,optimizer=tf.keras.optimizers.Adadelta(),metrics=['accuracy'])

    print(input_train.shape)
    hist = model.fit(input_train, labels_train, batch_size = 64, epochs = 100, verbose = 1)#, validation_data = (input_test,labels_test))
    model.save("mnist3.h5")

def give_random():
    r = random.randrange(len(input_test))
    result = []
    for i in range(len(input_test[r])):
        result.append([])
        for j in range(len(input_test[r][i])):
            result[i].append(input_test[r][j][i][0]*255)
    return result

model = keras.models.load_model('mnist2.h5')

def predict_digit(inputs):
    array = [[]]
    #print("inputs", inputs)
    for j in range(28):
        array[0].append([])
        for k in range(28):
            array[0][j].append(float(inputs[k][j])/255)
    array = numpy.array(array)
    #print("array",array)
    results = model.predict(array)
    return results[0]

def evaluate():
    score = model.evaluate(input_test,labels_test, verbose = 0)
    print("score", score)


format_data()
#make_model()
evaluate()
