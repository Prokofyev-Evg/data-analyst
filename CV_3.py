from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import numpy as np

optimizer = Adam()

def load_train(path):
    datagen = ImageDataGenerator(
        # horizontal_flip=True,
        # vertical_flip=True,
        # width_shift_range=0.2,
        # height_shift_range=0.2,
        # rotation_range=90,
        validation_split=0.25,
        rescale=1./255
    )

    train_datagen_flow = datagen.flow_from_directory(
        path,
        target_size=(150, 150),
        batch_size=32,
        class_mode='sparse',
        subset='training',
        seed=12345
    )

    return train_datagen_flow

def create_model(input_shape):
    model = Sequential()

    model.add(Conv2D(filters=4, kernel_size=(3, 3), padding='same', input_shape=input_shape, activation='relu'))
    model.add(Conv2D(filters=4, kernel_size=(3, 3), padding='same', strides=2, input_shape=(26, 26, 4), activation='relu'))
    model.add(Flatten())
    model.add(Dense(units=12, activation='softmax'))

    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', 
              metrics=['acc']) 

    return model

def train_model(model, train_data, test_data, batch_size=None, epochs=20,
               steps_per_epoch=None, validation_steps=None):
    model.fit(train_data, 
              validation_data=test_data,
              batch_size=batch_size, epochs=epochs,
              steps_per_epoch=steps_per_epoch,
              validation_steps=validation_steps,
              verbose=2, shuffle=True)

    return model