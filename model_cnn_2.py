# -*- coding: utf-8 -*-
"""model_cnn_2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/14JTVwYXYt7UpDQQB2DEuNHFSZCHzEx5O
"""

import tensorflow as tf
from tensorflow.keras.layers import Dense, Flatten, Conv2D, MaxPooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Sequential
import h5py
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img, array_to_img
import os
import pandas as pd
import matplotlib.pyplot as plt
print(os.getcwd())

from google.colab import drive
drive.mount('/content/drive')

IMG_WIDTH=256
IMG_HEIGHT=256
batch_size=32
train_dir = r'drive/MyDrive/Colab Notebooks/minor_dataset/train'
val_dir  = r'drive/MyDrive/Colab Notebooks/minor_dataset/test'
image_gen_train = ImageDataGenerator(rescale=1./255, 
                                    zoom_range=0.2, 
                                    rotation_range=65,
                                    shear_range=0.09,
                                    horizontal_flip=True,
                                    vertical_flip=True)
image_gen_val = ImageDataGenerator(rescale=1./255)

train_data_gen = image_gen_train.flow_from_directory(batch_size=batch_size,directory=train_dir,shuffle=True,target_size=(IMG_HEIGHT, IMG_WIDTH),class_mode='sparse')
val_data_gen = image_gen_val.flow_from_directory(batch_size=batch_size,directory=val_dir,target_size=(IMG_HEIGHT, IMG_WIDTH),class_mode='sparse')

print(train_data_gen.class_indices)

model = Sequential()

model.add(tf.keras.layers.InputLayer(input_shape=(IMG_HEIGHT, IMG_WIDTH, 3)))

model.add(Conv2D(filters=64, kernel_size=3, strides=(2, 2), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=128, kernel_size=4, strides=(2, 2), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(filters=256, kernel_size=4, strides=(2, 2), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(128, activation='sigmoid'))

model.add(Dense(2, activation='softmax'))

model.summary()

model.compile(loss='sparse_categorical_crossentropy', optimizer=tf.keras.optimizers.Adam(
    learning_rate=0.01,
    beta_1=0.9,
    beta_2=0.999,
    epsilon=1e-07,
), metrics=['accuracy'])
checkpoint_filepath = './cnn_2/checkpoint'
model_checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_filepath,
    verbose=1,
    save_weights_only=True,
    monitor='val_accuracy',
    mode='max',
    save_best_only=True)

with tf.device('/GPU:0'):
    # model.load_weights(checkpoint_filepath)
    history = model.fit(train_data_gen, epochs=20, batch_size=32, validation_data=val_data_gen,  callbacks=[model_checkpoint_callback])

model.load_weights(checkpoint_filepath)
model.evaluate(train_data_gen)
model.evaluate(val_data_gen)

print(history.history.keys())
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()
# "Loss"
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'validation'], loc='upper left')
plt.show()

model.save("model_cnn_2.h5")

