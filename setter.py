import ctypes
import os
import random
import shutil
import time


def set_wallpaper(path, mode, moveto):

    images = []
    for (_, _, files) in os.walk(path):
        images.extend(files)

    if len(images) == 0:
        return 0
    else: # Select a random image
        i = random.randint(0, len(images)-1)
        img_path = os.path.join(path, images[i])

    # Set wallpaper
    SPI_SETDESKWALLPAPER = 20
    success = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, img_path, 0)

    if not success:
        return -1

    time.sleep(0.5)
    # move image from new to data
    if mode == 1:
        shutil.move(img_path, moveto)

    return 1
