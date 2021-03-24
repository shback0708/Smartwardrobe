import matplotlib
from matplotlib import pyplot as plt

import glob
import os
import io
import scipy.misc
import numpy as np
from six import BytesIO
from PIL import Image, ImageDraw, ImageFont

import tensorflow as tf

from object_detection.utils import label_map_util
from object_detection.utils import config_util
from object_detection.utils import visualization_utils as viz_utils
from object_detection.builders import model_builder

import pathlib

pipeline_file = 'pipeline_file.config'
physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

filenames = list(pathlib.Path('models/').glob('*.index'))
filenames.sort()

def get_model_detection_function(model):
  """Get a tf.function for detection."""

  @tf.function
  def detect_fn(image):
    """Detect objects in image."""

    image, shapes = model.preprocess(image)
    prediction_dict = model.predict(image, shapes)
    detections = model.postprocess(prediction_dict, shapes)

    return detections, prediction_dict, tf.reshape(shapes, [-1])

  return detect_fn

class ClothingDetector:
    detect_fn = None

    def __init__(self):
        #recover our saved model
        self.pipeline_config = pipeline_file
        #generally you want to put the last ckpt from training in here
        model_dir = str(filenames[-1]).replace('.index','')
        configs = config_util.get_configs_from_pipeline_file(self.pipeline_config)
        model_config = configs['model']
        detection_model = model_builder.build(
            model_config=model_config, is_training=False)

        # Restore checkpoint
        ckpt = tf.compat.v2.train.Checkpoint(
            model=detection_model)
        ckpt.restore(os.path.join(model_dir)).expect_partial()

        self.detect_fn = get_model_detection_function(detection_model)

    def getLabels(self, image):
        #load image into np array
        (im_width, im_height) = image.size
        image_np = np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

        input_tensor = tf.convert_to_tensor(
            np.expand_dims(image_np, 0), dtype=tf.float32)
        
        detections, predictions_dict, shapes = self.detect_fn(input_tensor)

        print(detections, predictions_dict, shapes)

        #TODO (Henry): add classifier, visualization code for now
        configs = config_util.get_configs_from_pipeline_file(self.pipeline_config)
        #map labels for inference decoding
        label_map_path = configs['eval_input_config'].label_map_path
        label_map = label_map_util.load_labelmap(label_map_path)
        categories = label_map_util.convert_label_map_to_categories(
            label_map,
            max_num_classes=label_map_util.get_max_label_map_index(label_map),
            use_display_name=True)
        category_index = label_map_util.create_category_index(categories)
    
        label_id_offset = 1
        image_np_with_detections = image_np.copy()
        viz_utils.visualize_boxes_and_labels_on_image_array(
            image_np_with_detections,
            detections['detection_boxes'][0].numpy(),
            (detections['detection_classes'][0].numpy() + label_id_offset).astype(int),
            detections['detection_scores'][0].numpy(),
            category_index,
            use_normalized_coordinates=True,
            max_boxes_to_draw=8,
            min_score_thresh=0.3,
            agnostic_mode=False,
        )
        plt.figure(figsize=(12,16))
        plt.imshow(image_np_with_detections)
        plt.savefig('test.png')
        return None


if __name__ == '__main__':
    cd = ClothingDetector()
    path = "train/test4.jpg"
    img_data = tf.io.gfile.GFile(path, 'rb').read()
    image = Image.open(BytesIO(img_data))
    cd.getLabels(image)
    print("test completed.")