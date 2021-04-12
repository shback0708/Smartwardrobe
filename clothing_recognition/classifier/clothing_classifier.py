import tensorflow as tf
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

import random
from tensorflow.keras.preprocessing import image
from tensorflow.keras import models
import numpy as np
from six import BytesIO
# from PIL import Image
import os
from PIL import Image as pilimage

from colorthief import ColorThief

model_dir = "data/models/"
#TODO: this might not be everything
class_lookup = ['Anorak', 'Blazer', 'Blouse', 'Bomber', 'Button-Down', 'Caftan', 'Capris', 'Cardigan', 'Chinos', 'Coat', 'Coverup', 'Culottes', 'Cutoffs', 'Dress', 'Flannel', 'Gauchos', 'Halter', 'Henley', 'Hoodie', 'Jacket', 'Jeans', 'Jeggings', 'Jersey', 'Jodhpurs', 'Joggers', 'Jumpsuit', 'Kaftan', 'Kimono', 'Leggings', 'Onesie', 'Parka', 'Peacoat', 'Poncho', 'Robe', 'Romper', 'Sarong', 'Shorts', 'Skirt', 'Sweater', 'Sweatpants', 'Sweatshorts', 'Tank', 'Tee', 'Top', 'Trunks', 'Turtleneck']
height,width = 240,240

class ClothingClassifier:
    model = None

    def __init__(self):
        #load latest checkpoint
        fn = os.path.join(os.path.dirname(__file__), model_dir)
        all_subdirs = [os.path.join(os.path.dirname(__file__),model_dir+d) for d in os.listdir(fn) if os.path.isdir(os.path.join(os.path.dirname(__file__),model_dir+d))]
        print(all_subdirs)

        latest_subdir = max(all_subdirs, key=os.path.getmtime, default=None)
        if latest_subdir is not None:
            self.model = models.load_model(latest_subdir, compile=False)
        else:
            print("no model found")
            quit()
    
    def batchGetAttributes(self, imgs):
        processed = []
        if len(imgs) == 0:
            return []


        for img in imgs:
            img = img.resize((width, height))
            x = image.img_to_array(img)
            # x = x.reshape((1,) + x.shape)
            x /= 255.
            processed.append(x)

        results = self.model.predict(np.array(processed), batch_size=16)

        ret = []
        for i in range(len(processed)):
            top5 = np.argpartition(results[i], -5)[-5:]
            predicted_classes = []
            predicted_probabilities = []
            for j in range(5):
                predicted_classes.append(class_lookup[top5[j]])
                predicted_probabilities.append(results[i][top5[j]])
            ret.append((predicted_classes, predicted_probabilities))

        return ret

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
        top5 = np.argpartition(result_verbose[0], -5)[-5:]
        predicted_classes = []
        predicted_probabilities = []
        for i in range(5):
            predicted_classes.append(class_lookup[top5[i]])
            predicted_probabilities.append(result_verbose[0][top5[i]])
        # print(predicted_classes, predicted_probability)
        # predicted_class = class_lookup[np.argmax(result_verbose, axis=1)[0]]
        # predicted_probability = result_verbose[0][np.argmax(result_verbose, axis=1)[0]]

        # Get color
        imgfile = BytesIO()
        img.save(imgfile, format='jpeg')
        cf = ColorThief(imgfile)
        color = cf.get_color()
        # print(color)
        return predicted_classes, predicted_probabilities, color

import time
import csv
if __name__ == '__main__':
    valfile = "data/top5.csv"
    fields = ["Category", "top-5 acc", "time"]
    with open(valfile, 'w') as f:
        write = csv.writer(f)
        write.writerow(fields)
        cc = ClothingClassifier()
        test_dir = "data/test/"
        test_dir = os.path.join(os.path.dirname(__file__),test_dir)
        test_imgs = []
        total = 0
        correct = 0
        for path, subdirs, files in os.walk(test_dir):
            category = os.path.basename(os.path.normpath(path))
            print("category", category)
            category_total = 0
            category_correct = 0

            imgs = []
            start = time.time()
            for name in files:
                filepath = os.path.join(path, name)
                test_imgs.append(filepath)
                with pilimage.open(filepath).convert('RGB') as img:
                    imgs.append(img)

            predictions = cc.batchGetAttributes(imgs)
            for predicted_classes, predicted_probabilies in predictions:
                category_total += 1
                if category in predicted_classes:
                    category_correct += 1

            if category_total > 0:
                end = time.time()
                write.writerow([category_total, category_correct/category_total, end - start])
                print("total:", category_total, "accuracy:", category_correct/category_total, "time:", end - start)
            total += category_total
            correct += category_correct

    print("test completed, accuracy:", correct/total)