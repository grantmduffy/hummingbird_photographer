# https://www.tensorflow.org/tutorials/images/transfer_learning
import tensorflow as tf
from PIL import Image
from pathlib import Path
import numpy as np
import tensorflow_hub as hub
import random
from tensorflow.keras import models, layers
from tensorflow.keras.utils import to_categorical

label_dict = {'background': 0, 'hummingbird': 1}
IMAGE_SHAPE = (224, 224, 3)

labels_path = tf.keras.utils.get_file('ImageNetLabels.txt',
                                      'https://storage.googleapis.com/download.tensorflow.org/data/ImageNetLabels.txt')
imagenet_labels = list(np.array(open(labels_path).read().splitlines()))
hummingbird_index = imagenet_labels.index('hummingbird')

MODEL_SEL = False

if MODEL_SEL:
    # get the model
    classifier_url = "https://hub.tensorflow.google.cn/google/tf2-preview/mobilenet_v2/classification/2"

    model = tf.keras.Sequential([
        hub.KerasLayer(classifier_url, input_shape=IMAGE_SHAPE, trainable=True)
    ])
else:
    # Create the base model from the pre-trained model MobileNet V2
    model = tf.keras.applications.MobileNetV2(input_shape=IMAGE_SHAPE,
                                              include_top=False,
                                              weights='imagenet')
    # Freeze all the layers before the `fine_tune_at` layer
    model.summary()
    print(f'Number of layers: {len(model.layers)}')
    for layer in model.layers[:120]:
        layer.trainable = False
    model.summary()
    model.trainable = False
    model.summary()
    model = tf.keras.Sequential([model])
    model.add(layers.GlobalMaxPooling2D())
    model.add(layers.Dense(16, activation='relu'))
    model.add(layers.Dense(1, activation='sigmoid'))

model.summary()


model.layers[-1].trainable = True

# model.save('MobileNetV2')

# model, hummingbird_index = create_model()

def load_images(filelist):
    imgs = []
    for img_file in filelist:
        img = Image.open(str(img_file))
        img = img.resize(IMAGE_SHAPE[:2])
        imgs.append(np.array(img))
        labels.append(label_value)
    imgs_arr = np.array(imgs) / 255.0
    return imgs_arr
    
    
# load data
all_files = []
all_labels = []
for label_name, label_value in label_dict.items():
    dirpath = Path(f'training_data/{label_name}')
    files = list(dirpath.glob('*.jpg')) + list(dirpath.glob('*.JPG'))
    labels = [label_value] * len(files)
    all_files += files
    all_labels += labels

all_images = load_images(all_files)

# do prediction on current model
pred = model.predict(all_images)
pred_class = np.argmax(pred, -1)
pred_name = [imagenet_labels[pred_idx] for pred_idx in pred_class]


all_labels_binary = to_categorical(all_labels, num_classes=1001, dtype='float32')
# Alternatively, you can use the loss function `sparse_categorical_crossentropy` instead,
# which does expect integer targets.
model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.05, momentum=0.9),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True, label_smoothing=0.1),
              metrics=['accuracy'])
model.summary()
model.trainable

model.fit(all_images, all_labels_binary,
          epochs=10,
          steps_per_epoch=1,
          validation_split=0.2,
          shuffle=True)

# do prediction on new model
pred2 = model.predict(all_images)
pred2_class = np.argmax(pred2, -1)
pred_name2 = [imagenet_labels[pred_idx] for pred_idx in pred2_class]

model.save('MobileNetV2_retrained')

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open("humm.tflite", "wb").write(tflite_model)
print('converted')

print('done')
