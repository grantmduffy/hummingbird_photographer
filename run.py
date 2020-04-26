# Main run file - should take images and run inference
from time import sleep
from shutil import copy
from camera import capture_preview, capture
from mnv3_predict_tflite import predict_hum
from os import listdir

cap_folder = '/home/pi/shared/cap/'
hum_folder = '/home/pi/shared/hum/'
not_hum_folder = '/home/pi/shared/not_hum/'


def get_dir_count(dir):
    files = listdir(dir)
    if len(files) == 0:
        return 0
    num_str = [n.upper().replace('.JPG', '').replace('CAP', '').replace('HUM', '').replace('N', '') for n in files]
    nums = [int(s) for s in num_str if s.isdecimal()]
    return max(nums) + 1


cap_count = get_dir_count(cap_folder)
hum_count = get_dir_count(hum_folder)
not_hum_count = get_dir_count(not_hum_folder)


while True:
    img_path = capture_preview()
    copy(img_path, cap_folder + f'CAP{cap_count:06d}.JPG')
    cap_count += 1
    print(f'Capture Taken: {img_path}...', end='')
    if predict_hum(img_path):
        print('Hummingbird Found!!!')
        for file in capture():
            print(f'\tFile: {file}: ', end='')
            if predict_hum(file):
                print('Is Hummingbird')
                copy(file, hum_folder + f'HUM{hum_count:06d}.JPG')
                hum_count += 1
            else:
                print('Not Hummingbird')
                copy(file, not_hum_folder + f'NHUM{not_hum_count:06d}.JPG')
                not_hum_count += 1
    else:
        print('No Hummingbird')

    sleep(10)
