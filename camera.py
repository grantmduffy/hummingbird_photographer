# Used for controlling dslr via gphoto2
from sh import gphoto2 as gp


class Camera:

    def __getattr__(self, item):
        command = item.replace('_', '-')

        def ret_func(**kwargs):
            params = [f'--{command}'] + [x for y in zip([f'--{k}' for k in kwargs],
                                                        [f'{kwargs[k]}' for k in kwargs]) for x in y]
            print(params)
            return gp(params)

        return ret_func
        
        # return lambda **kwargs: gp([f'--{command}'] + [x for y in zip([f'--{k}' for k in kwargs],
        #                                                               [f'{kwargs[k]}' for k in kwargs]) for x in y])


camera = Camera()
