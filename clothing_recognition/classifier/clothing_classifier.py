import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

import random
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models
import numpy as np
from six import BytesIO as io
# from PIL import Image
import os
from PIL import Image as pilimage

from colorthief import ColorThief

model_dir = "data/models/"
class_lookup = ["Anorak", "Blazer", "Blouse", "Bomber", "Button-Down", "Caftan", "Capris", "Cardigan", "Chinos", "Coat, Coverup", "Culottes", "Cutoffs", "Dress", "Flannel", "Gauchos", "Halter", "Henley", "Hoodie", "Jacket", "Jeans", "Jeggings", "Jersey", "Jodhurs", "Joggers", "Jumpsuit", "Kaftan", "Kimono", "Leggings", "Onesie", "Parka", "Peacoat", "Poncho", "Robe", "Romper", "Sarong", "Shorts", "Skirt", "Sweater", "Sweatpants", "Sweatshorts", "Tank", "Tee", "Top", "Trunks", "Turtleneck"]
height,width = 224,224

class ClothingClassifier:
    model = None

    def __init__(self):
        #load latest checkpoint
        fn = os.path.join(os.path.dirname(__file__), model_dir)
        all_subdirs = [os.path.join(os.path.dirname(__file__),model_dir+d) for d in os.listdir(fn) if os.path.isdir(os.path.join(os.path.dirname(__file__),model_dir+d))]
        print(all_subdirs)

        latest_subdir = max(all_subdirs, key=os.path.getmtime, default=None)
        if latest_subdir is not None:
            self.model = models.load_model(latest_subdir)
        else:
            print("no model found")
            quit()
    
    def getAttributes(self, img):
        # Convert it to a Numpy array with target shape.
        img = img.resize((width, height))
        #img = image.load_img(img_path, target_size=(height, width))
        #x = np.array(img).astype(float)
        x = image.img_to_array(img)
        # Reshape
        x = x.reshape((1,) + x.shape)
        x /= 255.
        result_verbose = self.model.predict([x])
        print(result_verbose)
        top3 = np.argpartition(result_verbose[0], -3)[-3:]
        print(top3)
        for i in range(3):
            predicted_class = class_lookup[top3[i]]
            predicted_probability = result_verbose[0][top3[i]]
            print(predicted_class, predicted_probability)
        predicted_class = class_lookup[np.argmax(result_verbose, axis=1)[0]]
        predicted_probability = result_verbose[0][np.argmax(result_verbose, axis=1)[0]]

        # Get color
        imgfile = io.BytesIO()
        img.save(imgfile, 'format=jpg')
        cf = ColorThief(imgfile)
        color = cf.get_color()
        print(color)
        return predicted_class, predicted_probability, color

if __name__ == '__main__':
    cc = ClothingClassifier()
    test_dir = "data/test/"
    test_dir = os.path.join(os.path.dirname(__file__),test_dir)
    test_imgs = []
    for path, subdirs, files in os.walk(test_dir):
        for name in files:
            test_imgs.append(os.path.join(path, name))
    random_test_image = random.choice(test_imgs)
    img_data = tf.io.gfile.GFile(random_test_image, 'rb').read()
    image = pilimage.open(io.BytesIO(img_data))
    print(random_test_image)
    cc.getAttributes(image)
    print("test completed.")