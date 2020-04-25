# Main run file - should take images and run inference
from time import sleep
from shutil import copy
from camera import capture_preview, capture
from mnv3_predict import predict_hum

print('RUN')

while True:
    img_path = capture_preview('~/shared/')
    if predict_hum(img_path):
        # copy(img_path, '~/shared/hum/')
        for file in capture():
            if predict_hum(file):
                copy(file, '~/shared/hum/')
            else:
                copy(file, '~/shared/not_hum/')
    sleep(10)