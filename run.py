# Main run file - should take images and run inference
from time import sleep
from shutil import copy
from camera import capture
from mnv3_predict import predict_hum

print('RUN')

while True:
    img_path = capture('~/shared/')
    if predict_hum(img_path):
        copy(img_path, '~/shared/hum/')
    else:
        copy(img_path, '~/shared/not_hum/')
    sleep(10)