# https://www.tensorflow.org/tutorials/images/transfer_learning
import tensorflow as tf
from PIL import Image
from pathlib import Path
import numpy as np
import tensorflow_hub as hub

MODEL_SEL = True

IMAGE_SHAPE = (224, 224, 3)
label_dict = {'background': 0, 'hummingbird': 95}

labels_path = tf.keras.utils.get_file('ImageNetLabels.txt',
                                      'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = list(np.array(open(labels_path).read().splitlines()))

hummingbird_index = imagenet_labels.index('hummingbird')

if MODEL_SEL:
    # get the model
    classifier_url = "https://hub.tensorflow.google.cn/google/tf2-preview/mobilenet_v2/classification/2"

    model = tf.keras.Sequential([
        hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE, trainable=True)
    ])
else:
    # Create the base model from the pre-trained model MobileNet V2
    model = tf.keras.applications.MobileNetV2(input_shape=IMAGE_SHAPE,
                                              include_top=True,
                                              weights='imagenet')

print(len(model.layers))

# Freeze all the layers before the `fine_tune_at` layer
# for layer in model.layers[:120]:
#     layer.trainable = False

# model.save('MobileNetV2')

# load data
imgs = []
labels = []
for label_name, label_value in label_dict.items():
    dirpath = Path(f'images/{label_name}')
    files = list(dirpath.glob('*.jpg')) + list(dirpath.glob('*.JPG'))
    for img_file in files:
        img = Image.open(str(img_file))
        img = img.resize(IMAGE_SHAPE[:2])
        imgs.append(np.array(img))
        labels.append(label_value)

imgs_arr = np.array(imgs) / 255.0
labels_arr = np.array(labels)

# do prediction on current model
pred = model.predict(imgs_arr)
pred_class = np.argmax(pred, -1)
pred_name = [imagenet_labels[pred_idx] for pred_idx in pred_class]

from tensorflow.keras.utils import to_categorical
labels_binary = to_categorical(labels_arr, num_classes=1001, dtype='float32')
# ```
#
# Alternatively, you can use the loss function `sparse_categorical_crossentropy` instead,
# which does expect integer targets.
model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.005, momentum=0.9),
              loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True, label_smoothing=0.1),
              metrics=['accuracy'])
model.summary()

model.fit(imgs_arr, labels_binary,
          epochs=5,
          steps_per_epoch=1)

# do prediction on new model
pred2 = model.predict(imgs_arr)
pred2_class = np.argmax(pred2, -1)
pred_name2 = [imagenet_labels[pred_idx] for pred_idx in pred2_class]

model.save('MobileNetV2_retrained')

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open("humm.tflite", "wb").write(tflite_model)
print('converted')

print('done')
