import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

from PIL import Image
from pathlib import Path

# get the model
classifier_url = "https://hub.tensorflow.google.cn/google/tf2-preview/mobilenet_v2/classification/2"

IMAGE_SHAPE = (224, 224)

classifier = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
])

# get the labels
labels_path = tf.keras.utils.get_file('ImageNetLabels.txt',
                                      'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = list(np.array(open(labels_path).read().splitlines()))

hummingbird_index = imagenet_labels.index('hummingbird')
