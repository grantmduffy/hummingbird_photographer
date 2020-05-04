import sys
import numpy as np
from PIL import Image

win32 = sys.platform == 'win32'
if win32:
    import tensorflow as tf
    from pathlib import Path
else:
    import tflite_runtime.interpreter as tflite


# Load TFLite model and allocate tensors.
if win32:
    interpreter = tf.lite.Interpreter(model_path='humm.tflite')
else:
    interpreter = tflite.Interpreter(model_path="humm.tflite")
interpreter.allocate_tensors()

# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Test the TensorFlow Lite model on random input data.
input_shape = input_details[0]['shape']
# input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
# interpreter.set_tensor(input_details[0]['index'], input_data)
#
# interpreter.invoke()
#
# The function `get_tensor()` returns a copy of the tensor data.
# Use `tensor()` in order to get a pointer to the tensor.
# tflite_results = interpreter.get_tensor(output_details[0]['index'])


def predict_hum(filename):
    img = Image.open(filename).resize(input_shape[2:0:-1])
    img_data = np.array(img, dtype=np.float32) / 255.0

    interpreter.set_tensor(input_details[0]['index'], img_data[np.newaxis, ...])
    interpreter.invoke()

    # The function `get_tensor()` returns a copy of the tensor data.
    # Use `tensor()` in order to get a pointer to the tensor.
    tflite_results = interpreter.get_tensor(output_details[0]['index'])
    predicted_class = np.round(tflite_results[0])
    return predicted_class


if __name__ == '__main__':

    for label in ['background', 'hummingbird']:
        files = Path(f'training_data/{label}')
        print(files)
        files = files.glob('*.JPG')
        for img_file in files:
            print(f'{str(img_file)}, label: {label}, prediction: {predict_hum(str(img_file))}')
