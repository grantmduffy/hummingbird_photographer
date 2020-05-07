from os import listdir
from PIL import Image, ImageDraw
import cv2
import numpy as np

img_path = '//192.168.0.48/shared/cap/'
files = sorted(listdir(img_path))
n = len(files)
fps = 20

img0 = Image.open(img_path + files[0])
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
writer = cv2.VideoWriter('cap_lapse.avi', fourcc, fps, img0.size)

prog_steps = 100
progress = -1
for i, fname in enumerate(files):
    p = prog_steps * i // n
    if p > progress:
        progress = p
        s = f'\rframe:{i: >5}/{n}|' + u'\u2588' * progress + '-' * (prog_steps - progress) + f'|{progress}%'
        print(s, end='')
    try:
        img = Image.open(img_path + fname)
        d = ImageDraw.Draw(img)
        d.text((20, 20), fname)
        arr = np.array(img)[:, :, ::-1]
        writer.write(arr)
    except Exception as e:
        print(f'Failed on frame {i}')
        print(e, '\n')

writer.release()


