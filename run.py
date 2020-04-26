# Main run file - should take images and run inference
from time import sleep
from shutil import copy
from camera import capture_preview, capture
from mnv3_predict_tflite import predict_hum

print('RUN')

while True:
    img_path = capture_preview('/home/pi/shared/')
    print(f'Capture Taken: {img_path}...', end='')
    if predict_hum(img_path):
        print('Hummingbird Found!!!')
        # copy(img_path, '/home/pi/shared/hum/')
        for file in capture():
            print(f'\tFile: {file}: ', end='')
            if predict_hum(file):
                print('Is Hummingbird')
                copy(file, '/home/pi/shared/hum/')
            else:
                print('Not Hummingbird')
                copy(file, '/home/pi/shared/not_hum/')
    else:
        print('No Hummingbird')

    sleep(10)
