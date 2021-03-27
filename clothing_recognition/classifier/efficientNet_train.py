import tensorflow as tf

physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

import tensorflow.keras

from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras import optimizers
from tensorflow.keras.callbacks import ModelCheckpoint
from tensorflow.keras.callbacks import TensorBoard
import os
import glob
import shutil
import sys
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from IPython.display import Image
import random

# Options: EfficientNetB0, EfficientNetB1, EfficientNetB2, EfficientNetB3
# Higher the number, the more complex the model is.

#Choose
#EfficientNetB0, EfficientNetB1, EfficientNetB2, EfficientNetB3
import tensorflow.keras.applications.efficientnet as Net

height = 224
width = 224
input_shape = (height, width, 3)

train_dir = "data/train/"
valid_dir = "data/validate/"
test_dir = "data/test/"
model_dir = "data/models/"

batch_size = 4

conv_base = Net.EfficientNetB0(weights='imagenet', include_top=False, input_shape=input_shape)


from tensorflow.keras.preprocessing.image import ImageDataGenerator

train_datagen = ImageDataGenerator(rescale=1.0 / 255, preprocessing_function=Net.preprocess_input)

test_datagen = ImageDataGenerator(rescale=1.0 / 255, preprocessing_function=Net.preprocess_input)

train_generator = train_datagen.flow_from_directory(
        # This is the target directory
        train_dir,
        # All images will be resized to target height and width.
        target_size=(height, width),
        batch_size=batch_size,
        # Since we use categorical_crossentropy loss, we need categorical labels
        class_mode='categorical')

validation_generator = test_datagen.flow_from_directory(
        valid_dir,
        target_size=(height, width),
        batch_size=batch_size,
        class_mode='categorical')

print(train_generator.class_indices)

epochs = 20

NUM_TRAIN = sum([len(files) for r, d, files in os.walk(train_dir)])
NUM_TEST = sum([len(files) for r, d, files in os.walk(valid_dir)])

dropout_rate = 0.2

num_classes = len(os.listdir(train_dir))
print('building network for ' + str(num_classes) + ' classes')

fn = os.path.join(os.path.dirname(__file__), model_dir)
all_subdirs = [os.path.join(os.path.dirname(__file__),model_dir+d) for d in os.listdir(fn) if os.path.isdir(os.path.join(os.path.dirname(__file__),model_dir+d))]
print(all_subdirs)

initial_epoch = 0
latest_subdir = max(all_subdirs, key=os.path.getmtime, default=None)
if latest_subdir is not None:
    model = models.load_model(latest_subdir)
    print("loaded model:", latest_subdir)
    initial_epoch = int(latest_subdir[-3:])
    print("initial_epoch:", initial_epoch)
else:
    model = models.Sequential()
    model.add(conv_base)
    model.add(layers.GlobalMaxPooling2D(name="gap"))
    model.add(layers.BatchNormalization())
    # model.add(layers.Flatten(name="flatten"))
    if dropout_rate > 0:
        model.add(layers.Dropout(dropout_rate, name="dropout_out"))
    # model.add(layers.Dense(256, activation='relu', name="fc1"))
    model.add(layers.Dense(num_classes, activation='softmax', name="fc_out"))

    optimizer = tf.keras.optimizers.Adam()
    model.compile(
        optimizer=optimizer, loss="categorical_crossentropy", metrics=["accuracy"]
    )

model.summary()

print('This is the number of trainable layers '
      'before freezing the conv base:', len(model.trainable_weights))

#freeze all but last three
for layer in model.layers[:-3]:
    print(layer.name)
    layer.trainable = False

print('This is the number of trainable layers '
      'after freezing the conv base:', len(model.trainable_weights))


filepath= model_dir + "/{epoch:03d}"
checkpoint = ModelCheckpoint(filepath, save_weights_only=False)
tensorboard_callback = TensorBoard(log_dir="./logs", update_freq=1000)

if __name__ == '__main__':
    history = model.fit(
        train_generator,
        steps_per_epoch= NUM_TRAIN / batch_size,
        epochs=epochs,
        callbacks=[checkpoint, tensorboard_callback],
        validation_data=validation_generator,
        validation_steps=NUM_TEST / batch_size,
        verbose=1,
        initial_epoch=initial_epoch)
