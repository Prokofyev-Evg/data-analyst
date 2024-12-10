import os
import numpy as np
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Conv2D, Flatten, Dense, AveragePooling2D, GlobalAveragePooling2D, Dropout
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet import ResNet50

def load_train(path):
    labels_df = pd.read_csv(os.path.join(path, 'labels.csv'))
    datagen = ImageDataGenerator(
        validation_split=0.25,
        rescale=1./255
    )
    datagen_flow = datagen.flow_from_dataframe(
        dataframe=labels_df,
        directory=os.path.join(path, 'final_files/'), 
        target_size=(224, 224),
        x_col='file_name',
        y_col='real_age',
        batch_size=16,
        class_mode='raw',
        subset='training',
        seed=12345
    )
    return datagen_flow

def load_test(path):
    labels_df = pd.read_csv(os.path.join(path, 'labels.csv'))
    datagen = ImageDataGenerator(
        validation_split=0.25,
        rescale=1./255
    )
    datagen_flow = datagen.flow_from_dataframe(
        dataframe=labels_df,
        directory=os.path.join(path, 'final_files/'), 
        target_size=(224, 224),
        x_col='file_name',
        y_col='real_age',
        batch_size=16,
        class_mode='raw',
        subset='validation',
        seed=12345
    )
    return datagen_flow


def create_model(input_shape):
    backbone = ResNet50(input_shape=input_shape,
                        weights='/datasets/keras_models/resnet50_weights_tf_dim_ordering_tf_kernels_notop.h5',
                        include_top=False)
    model = Sequential()
    model.add(backbone)
    model.add(Conv2D(filters=8, kernel_size=(3, 3), padding='same', input_shape=(150, 150, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(2, 2)))
    model.add(Conv2D(filters=6, kernel_size=(3, 3), padding='same', input_shape=(150, 150, 3), activation='relu'))
    model.add(AveragePooling2D(pool_size=(2, 2)))
    model.add(Conv2D(filters=4, kernel_size=(3, 3), padding='same', input_shape=(150, 150, 3), activation='relu'))
    model.add(GlobalAveragePooling2D())
    model.add(Dense(1, activation='relu'))
    model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mae']) 
    return model

def train_model(model, train_data, test_data, batch_size=16, epochs=10,
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