import tensorflow as tf
from PIL import Image
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt

from simple_model import create_model, INPUT_SIZE

label_dict = {'background': 0, 'hummingbird': 1}


def load_images(filelist):
    imgs = []
    for img_file in filelist:
        img = Image.open(str(img_file))
        img = img.resize(INPUT_SIZE[:2])
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
all_labels = np.array(all_labels).astype('float')

model = create_model()

model.compile(optimizer=tf.keras.optimizers.SGD(lr=0.02, momentum=0.5),
              loss=tf.keras.losses.BinaryCrossentropy(from_logits=True, label_smoothing=0.1),
              metrics=['accuracy'])
model.summary()

if False:
    try:
        model.load_weights('simple.h5')
        print('Successfully loaded weights from simple.h5')
    except FileNotFoundError as e:
        print('Failed to load weights from simple.h5')

h = model.fit(all_images, all_labels,
          epochs=10,
          steps_per_epoch=1,
          validation_split=0.2,
          shuffle=True)

# do prediction on new model
pred2 = model.predict(all_images)
pred2_class = np.round(pred2)

model.save('simple')
model.save_weights('simple.h5')

# Convert the model.
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()
open("simple.tflite", "wb").write(tflite_model)
print('converted')

print('done')
print(h.history)

# Plotting training progress
plt.figure()
plt.subplot(211)
plt.plot(h.history['loss'], label='Training Loss')
plt.plot(h.history['val_loss'], label='Validation Loss')
plt.subplot(212)
plt.plot(h.history['accuracy'], label='Training Accuracy')
plt.plot(h.history['val_accuracy'], label='Validation Accuracy')
plt.legend()
plt.show()
