# Main run file - should take images and run inference
from time import sleep
from shutil import copy
from camera import capture_preview, capture, camera
from mnv3_predict_tflite import predict_hum
from os import listdir
import argparse

cap_folder = '/home/pi/shared/cap/'
hum_folder = '/home/pi/shared/hum/'
not_hum_folder = '/home/pi/shared/not_hum/'

parser = argparse.ArgumentParser()
parser.add_argument('--burst', type=int, default=5)
parser.add_argument('--delay', type=float, default=3.0)
args = parser.parse_args()
camera.set_config('burstnumber', args.burst)


def get_dir_count(dir):
    files = listdir(dir)
    num_str = [n.upper().replace('.JPG', '').replace('CAP', '').replace('HUM', '').replace('N', '') for n in files]
    nums = [int(s) for s in num_str if s.isdecimal()]
    if len(nums) == 0:
        return 0
    return max(nums) + 1


cap_count = get_dir_count(cap_folder)
hum_count = get_dir_count(hum_folder)
not_hum_count = get_dir_count(not_hum_folder)


while True:
    img_path = capture_preview()
    path = copy(img_path, cap_folder + f'CAP{cap_count:06d}.JPG')
    cap_count += 1
    print(f'Capture Taken: {path}...', end='')
    if predict_hum(img_path):
        print('Hummingbird Found!!!')
        for file in capture():
            print(f'\tFile: {file}: ', end='')
            if predict_hum(file):
                print('Is Hummingbird --> ', end='')
                path = copy(file, hum_folder + f'HUM{hum_count:06d}.JPG')
                print(path)
                hum_count += 1
            else:
                print('Not Hummingbird --> ', end='')
                path = copy(file, not_hum_folder + f'NHUM{not_hum_count:06d}.JPG')
                print(path)
                not_hum_count += 1
    else:
        print('No Hummingbird')

    sleep(args.delay)
