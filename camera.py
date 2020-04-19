# Used for controlling dslr via gphoto2
from sh import gphoto2 as gp


class Camera:

    def __getattr__(self, item):
        command = item.replace('_', '-')
        args_gen = lambda kwargs: ' '.join([f'--{k} {kwargs[k]}' for k in kwargs])
        return lambda **kwargs: gp(f'--{command} {args_gen(kwargs)}')


camera = Camera()
