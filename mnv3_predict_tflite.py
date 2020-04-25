# import tensorflow as tf
import tflite_runtime.interpreter as tflite
import numpy as np

from PIL import Image


# get the model
IMAGE_SHAPE = (224, 224)

# get the labels
# labels_path = tf.keras.utils.get_file('ImageNetLabels.txt',
#                                       'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
# imagenet_labels = list(np.array(open(labels_path).read().splitlines()))
# hummingbird_index = imagenet_labels.index('hummingbird')
hummingbird_index = 95

# Load TFLite model and allocate tensors.
interpreter = tflite.Interpreter(model_path="humm.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test the TensorFlow Lite model on random input data.
# input_shape = input_details[0]['shape']
# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# interpreter.set_tensor(input_details[0]['index'], input_data)
#
# interpreter.invoke()
#
# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
# tflite_results = interpreter.get_tensor(output_details[0]['index'])


def predict_hum(filename):
    img = Image.open(filename).resize((224, 224))
    img_data = np.array(img, dtype=np.float32) / 255.0

    interpreter.set_tensor(input_details[0]['index'], img_data[np.newaxis, ...])
    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    tflite_results = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.argmax(tflite_results[0], axis=-1)
    return predicted_class == hummingbird_index

#
# filename = 'images/humm1.jpg'
# # filename = 'images/birdfeeder.jpg'
# if predict_hum(filename):
#     print("Yes, it's a hummingbird")
# else:
#     print("No go - no hummingbird")
