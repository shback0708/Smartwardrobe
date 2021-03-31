import tensorflow as tf
import sys
import os
from six import BytesIO
from PIL import Image
from matplotlib import pyplot as plt
import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(__file__),'detector'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__),'classifier'))
from detector import clothing_detector as cd
from classifier import clothing_classifier as cc

# finds an returns num outfit images that best fit given labels online
class ClothingRecognitionModel:
    detector = None
    classifier = None

    def __init__(self):
        self.detector = cd.ClothingDetector()
        self.classifier = cc.ClothingClassifier()

    def getLabels(self, image):
        detections, c_index = self.detector.getLabels(image)
        bboxes = detections['detection_boxes'][0].numpy()
        classes = detections['detection_classes'][0].numpy()
        scores = detections['detection_scores'][0].numpy()
        for i in range(3):
            plt.figure(figsize=(12,16))
            ymin,xmin,ymax,xmax = bboxes[i]
            im_width, im_height = image.size
            dimensions = (min(xmin * im_width, im_width), 
                          min(ymin * im_height, im_height),
                          min(xmax * im_width, im_width), 
                          min(ymax * im_height, im_height))
            print(image.size)
            print(dimensions)
            cropped_img = image.crop(dimensions)
            cropped_img.save('cropped' + str(i) + '.png')
            predicted_class, probability = self.classifier.getAttributes(cropped_img)
            print("detector prediction:", c_index[classes[i]], "classifier predicion:", predicted_class)
            print("detector acc:", scores[i], "classifier acc:", probability)
if __name__ == '__main__':
    crm = ClothingRecognitionModel()
    image = Image.open('c:/Users/linhe/OneDrive/Documents/GitHub/Smartwardrobe/clothing_recognition/classifier/data/test/Jacket/00011117.jpg').convert("RGB")
    crm.getLabels(image)
    print("test completed.")