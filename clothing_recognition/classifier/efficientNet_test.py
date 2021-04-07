import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

import random
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models
import numpy as np

import os

model_dir = "data/models/"
test_dir = "data/test/"
class_lookup = ["Anorak", "Blazer", "Blouse", "Bomber", "Button-Down", "Caftan", "Capris", "Cardigan", "Chinos", "Coat, Coverup", "Culottes", "Cutoffs", "Dress", "Flannel", "Gauchos", "Halter", "Henley", "Hoodie", "Jacket", "Jeans", "Jeggings", "Jersey", "Jodhurs", "Joggers", "Jumpsuit", "Kaftan", "Kimono", "Leggings", "Onesie", "Parka", "Peacoat", "Poncho", "Robe", "Romper", "Sarong", "Shorts", "Skirt", "Sweater", "Sweatpants", "Sweatshorts", "Tank", "Tee", "Top", "Trunks", "Turtleneck"]
height,width = 240,240

fn = os.path.join(os.path.dirname(__file__), model_dir)
all_subdirs = [os.path.join(os.path.dirname(__file__),model_dir+d) for d in os.listdir(fn) if os.path.isdir(os.path.join(os.path.dirname(__file__),model_dir+d))]
print(all_subdirs)

latest_subdir = max(all_subdirs, key=os.path.getmtime, default=None)
if latest_subdir is not None:
    model = models.load_model(latest_subdir, compile=False)
else:
    print("no model found")
    quit()

def predict_image(img_path):
    # Read the image and resize it
    img = image.load_img(img_path, target_size=(height, width))
    # Convert it to a Numpy array with target shape.
    x = image.img_to_array(img)
    # Reshape
    x = x.reshape((1,) + x.shape)
    x /= 255.
    result_verbose = model.predict([x])
    predicted_class = class_lookup[np.argmax(result_verbose, axis=1)[0]]
    predicted_probability = result_verbose[0][np.argmax(result_verbose, axis=1)[0]]

    return predicted_class ,predicted_probability

if __name__ == '__main__':
    test_dir = os.path.join(os.path.dirname(__file__),test_dir)
    test_imgs = []
    for path, subdirs, files in os.walk(test_dir):
        for name in files:
            test_imgs.append(os.path.join(path, name))
    
    random_test_image = random.choice(test_imgs)
    print(random_test_image)
    print(predict_image(random_test_image))