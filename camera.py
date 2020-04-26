# Used for controlling dslr via gphoto2

from sh import gphoto2 as gp
from os import system

burst_number = 5
dcim_folder = '/store_00010001/DCIM/100D5100/'


class Camera:

    def __getattr__(self, item):
        return lambda **kwargs: gp([f'--{item.replace("_", "-")}'] +
                                   [x for y in zip([f'--{k}' for k in kwargs],
                                                   [f'{kwargs[k]}' for k in kwargs]) for x in y])

    def set_config(self, arg, value):
        return gp(['--set-config', f'{arg}={value}'])

    def get_config(self, arg):
        return gp(['--get-config', f'{arg}'])


camera = Camera()
camera.set_config('burstnumber', burst_number)
camera.set_config('capturemode', 1)


def capture_preview():
    try:
        system('rm capture_preview.jpg')
        # rm('./capture_preview.jpg')
    except Exception as e:
        print('Failed to remove current images')
        print(e)
    camera.capture_preview()
    return './capture_preview.jpg'


def capture():
    try:
        system('rm DSC_*.JPG')
        # rm('DSC*.JPG')
    except Exception as e:
        print('Failed to remove current images')
        print(e)
    camera.delete_all_files(folder=dcim_folder)
    camera.capture_image()
    s = camera.get_all_files()
    camera.delete_all_files(folder=dcim_folder)
    return [line.split(' ')[3].strip() for line in s.splitlines(True) if line[-1] != '\r']
