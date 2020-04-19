# Used for controlling dslr via gphoto2
from sh import gphoto2 as gp


class Camera:

    def __getattr__(self, item):
        arg = item.replace('_', '-')
        return lambda: gp(f'--{arg}')


camera = Camera()
