# Main run file - should take images and run inference
from time import sleep
from shutil import copy
from camera import capture_preview, capture
from mnv3_predict_tflite import predict_hum

print('RUN')

while True:
    img_path = capture_preview('/home/pi/shared/')
    if predict_hum(img_path):
        # copy(img_path, '/home/pi/shared/hum/')
        for file in capture():
            if predict_hum(file):
                copy(file, '/home/pi/shared/hum/')
            else:
                copy(file, '/home/pi/shared/not_hum/')
    sleep(10)
