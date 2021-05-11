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

margin = 0.05
# finds an returns num outfit images that best fit given labels online
class ClothingRecognitionModel:
    detector = None
    classifier = None

    def __init__(self):
        self.detector = cd.ClothingDetector()
        self.classifier = cc.ClothingClassifier()

    def batchGetLabels(self, images):
        cropped_imgs = []
        for image in images:
            detections, c_index = self.detector.getLabels(image)
            bboxes = detections['detection_boxes'][0].numpy()
            classes = detections['detection_classes'][0].numpy()
            scores = detections['detection_scores'][0].numpy()
            for i in range(3):
                ymin,xmin,ymax,xmax = bboxes[i]
                ymin = max(ymin-margin,0)
                xmin = max(xmin-margin,0)
                ymax = min(ymax+margin,1)
                xmax = min(xmax+margin,1)
                im_width, im_height = image.size
                dimensions = (min(xmin * im_width, im_width), 
                            min(ymin * im_height, im_height),
                            min(xmax * im_width, im_width), 
                            min(ymax * im_height, im_height))
                cropped_img = image.crop(dimensions)
                cropped_img.save("cropped"+str(i) + ".jpg")
                cropped_imgs.append(cropped_img)
        
        flat_labels = self.classifier.batchGetAttributes(cropped_imgs)
        # need to make it 2d array again
        ret = []
        for i in range(len(images)):
            grouped = []
            for j in range(3):
                grouped.append(flat_labels[i * 3 + j])
            ret.append(grouped)
        print(ret)
        return ret
            
    def getLabels(self, image):
        return self.batchGetLabels([image])[0]

if __name__ == '__main__':
    crm = ClothingRecognitionModel()
    image = Image.open('test.jpg').convert("RGB")
    crm.getLabels(image)
    print("test completed.")