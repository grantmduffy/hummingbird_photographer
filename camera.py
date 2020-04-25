# Used for controlling dslr via gphoto2

from sh import gphoto2 as gp
from sh import rm
from shutil import copy

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


def capture_preview(save_path=None):
    try:
        rm('capture_preview.jpg')
    except:
        pass
    camera.capture_preview()
    if save_path is not None:
        return copy('capture_preview.jpg', save_path)
    return './capture_preview.jpg'


def capture():
    try:
        rm('DSC*.JPG')
    except:
        pass
    camera.delete_all_files(folder=dcim_folder)
    camera.capture_image()
    s = camera.get_all_files()
    return [line.split(' ')[3] for line in s.splitlines(True) if line[-1] != '\r']
