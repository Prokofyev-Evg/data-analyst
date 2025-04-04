from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
import numpy as np

optimizer = Adam()

def load_train(path):
    features_train = np.load(path + 'train_features.npy')
    target_train = np.load(path + 'train_target.npy')
    features_train = features_train.reshape(-1, 28, 28, 1) / 255.0
    return features_train, target_train

def create_model(input_shape):
    model = Sequential()

    model.add(Conv2D(filters=4, kernel_size=(3, 3), padding='same', input_shape=input_shape, activation='relu'))
    model.add(Conv2D(filters=4, kernel_size=(3, 3), padding='same', strides=2, input_shape=(26, 26, 4), activation='relu'))
    model.add(Flatten())
    model.add(Dense(units=10, activation='softmax'))

    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', 
              metrics=['acc']) 

    return model

def train_model(model, train_data, test_data, batch_size=32, epochs=50,
               steps_per_epoch=None, validation_steps=None):

    features_train, target_train = train_data
    features_test, target_test = test_data
    model.fit(features_train, target_train, 
              validation_data=(features_test, target_test),
              batch_size=batch_size, epochs=epochs,
              steps_per_epoch=steps_per_epoch,
              validation_steps=validation_steps,
              verbose=2, shuffle=True)

    return model