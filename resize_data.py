from PIL import Image
from os import listdir

input_path = '//192.168.0.48/shared/training_data/'
output_path = '//192.168.0.48/shared/training_data_small/'
# output_path = './data/'

sub_folders = ['hum/', 'not_hum/']

small_size = (220, 148)

for folder in sub_folders:
    files = listdir(input_path + folder)
    for i, fname in enumerate(files):
        Image.open(input_path + folder + fname).resize(small_size).save(output_path + folder + f'IMG{i:06d}.JPG')