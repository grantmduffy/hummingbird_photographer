# Used for controlling dslr via gphoto2
from sh import gphoto2 as gp


class Camera:

    def __getattr__(self, item):
        return lambda **kwargs: gp([f'--{item.replace("_", "-")}'] +
                                   [x for y in zip([f'--{k}' for k in kwargs],
                                                   [f'{kwargs[k]}' for k in kwargs]) for x in y])


camera = Camera()
