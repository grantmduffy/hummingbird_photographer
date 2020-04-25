import tensorflow as tf
import tensorflow_hub as hub


# get the model
classifier_url = "https://hub.tensorflow.google.cn/google/tf2-preview/mobilenet_v2/classification/2"

IMAGE_SHAPE = (224, 224)

model = tf.keras.Sequential([
    hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE+(3,))
])

model.save('humm_model')
print('model saved to humm_model')

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open("humm.tflite", "wb").write(tflite_model)
print('converted')
