import mnv2
import tensorflow as tf
# from tensorflow.keras.preprocessing.image import ImageDataGenerator
from pathlib import Path
from PIL import Image
import numpy as np


# classes = [''] * 1001
# classes[0] = 'background'
# classes[95] = 'hummingbird'
# datagen = ImageDataGenerator(rescale=1/255.0)
# data_generator = datagen.flow_from_directory(
#     'training_data',
#     target_size=(224, 224),
#     batch_size=32,
#     class_mode='categorical',
#     classes=classes
# )

# read in data
img_data = []
counts = []
for i, label_path in enumerate(Path('training_data').iterdir()):
    img_data.append([])
    for img_file in label_path.glob('*.jpg'):
        img = Image.open(str(img_file)).resize((224, 224))
        img_data[i].append(np.array(img) / 255.0)
    counts.append(len(img_data[i]))
img_data = np.concatenate(img_data)

label_data0 = np.zeros(counts[0])
label_data95 = np.ones(counts[1]) * 95
label_data = np.concatenate([label_data0, label_data95]).astype(np.int)
labels = np.zeros((label_data.shape[0], 1001))
labels[np.arange(label_data.shape[0]), label_data.flatten()] = 1

# model, humm_idx = mnv2.create_model()

model = tf.keras.models.load_model('humm_model')
model.compile()

results = model.predict(img_data)
preds = np.argmax(results, axis=-1)
print(results)

print('done')
