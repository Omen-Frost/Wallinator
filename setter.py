import ctypes
import os
import random
import shutil
import time


def set_wallpaper(query, mode, log):

    data_path = os.getcwd() + "\\data"
    q_path = os.path.join(data_path, query)
    images = []
    done = False
    img_path = -1

    # Select image for wallpaper, either random or from current query, depending on mode
    if mode == 1:
        if os.path.exists(q_path):
            for files in os.listdir(q_path):
                if files[-4:] == ".jpg":
                    images.append(files)
        if len(images) != 0:
            img_path = os.path.join(q_path, random.choice(images))
            done = True

    if not done:
        # choose a random dir
        L = [folder for folder in os.listdir(
            data_path) if os.path.isdir(os.path.join(data_path, folder))]
        folder = random.choice(L)
        for files in os.listdir(os.path.join(data_path, folder)):
            if files[-4:] == ".jpg":
                images.append(files)
                # print(files)
        # print(images)
        # print(random.choice(images))
        if len(images) != 0:
            img_path = os.path.join(os.path.join(
                data_path, folder), random.choice(images))
            done = True

    if not done:
        print("skip", file=log, flush=True)
        return

    # Set wallpaper
    SPI_SETDESKWALLPAPER = 20
    success = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, img_path, 0)

    if not success:
        print("err: set failed", file=log, flush=True)
        return
    print("set " + img_path, file=log, flush=True)

    return
