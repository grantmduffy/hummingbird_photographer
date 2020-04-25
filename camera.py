# Used for controlling dslr via gphoto2

from sh import gphoto2 as gp
from sh import rm
from shutil import copy


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


def capture(save_path=None):
    try:
        rm('capture_preview.jpg')
    except:
        pass
    camera.capture_preview()
    if save_path is not None:
        return copy('capture_preview.jpg', save_path)
    return './capture_preview.jpg'
