from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, AveragePooling2D, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet import ResNet50
import numpy as np


def load_train(path):
    datagen = ImageDataGenerator(
        # horizontal_flip=True,
        # vertical_flip=True,
        # width_shift_range=0.2,
        # height_shift_range=0.2,
        # rotation_range=90,
        validation_split=0.1,
        rescale=1./255
    )
    train_datagen_flow = datagen.flow_from_directory(
        path,
        target_size=(150, 150),
        batch_size=32,
        class_mode='sparse',
        seed=12345
    )
    return train_datagen_flow

def create_model(input_shape):
    backbone = ResNet50(input_shape=input_shape,
                        weights='/datasets/keras_models/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
                        include_top=False)
    # backbone.trainable = False
    model = Sequential()
    model.add(backbone)
    model.add(Conv2D(filters=8, kernel_size=(3, 3), padding='same', input_shape=(150, 150, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(2, 2)))
    model.add(Conv2D(filters=6, kernel_size=(3, 3), padding='same', input_shape=(150, 150, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(2, 2)))
    model.add(Conv2D(filters=4, kernel_size=(3, 3), padding='same', input_shape=(150, 150, 3), activation='relu'))
    model.add(GlobalAveragePooling2D())
    model.add(Dense(12, activation='softmax'))
    model.compile(optimizer=Adam(), loss='sparse_categorical_crossentropy', metrics=['acc']) 
    return model

def train_model(model, train_data, test_data, batch_size=None, epochs=6,
               steps_per_epoch=None, validation_steps=None):
    model.fit(train_data, 
              validation_data=test_data,
              batch_size=batch_size,
              epochs=epochs,
              steps_per_epoch=steps_per_epoch,
              validation_steps=validation_steps,
              verbose=2,
              shuffle=True)

    return model