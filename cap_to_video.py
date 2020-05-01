from os import listdir
from PIL import Image, ImageDraw
import cv2
import numpy as np

img_path = '//192.168.0.48/share/cap/'
n = len(listdir(img_path))
fps = 20

img0 = Image.open(img_path + f'CAP{0:06d}.JPG')
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
writer = cv2.VideoWriter('cap_lapse.avi', fourcc, fps, img0.size)

prog_steps = 100
progress = -1
for i in range(n):
    p = prog_steps * i // n
    if p > progress:
        progress = p
        s = f'\rframe:{i: >5}/{n}|' + u'\u2588' * progress + '-' * (prog_steps - progress) + f'|{progress}%'
        print(s, end='')
    img = Image.open(img_path + f'CAP{i:06d}.JPG')
    d = ImageDraw.Draw(img)
    d.text((20, 20), f'CAP{i:06d}.JPG')
    arr = np.array(img)[:, :, ::-1]
    writer.write(arr)

writer.release()


