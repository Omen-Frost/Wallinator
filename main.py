import setter
import os
import time
import get_images
import threading
from threading import Thread


# parses config file to read settings and set search parameters
def parse(lines):
    d = {}
    for line in lines:
        s = line[0]
        l = line.find('(')
        r = line.rfind(')')
        if l >= r:
            continue
        if s == '1':
            try:
                d['frequency'] = int(line[l+1:r].strip())
            except:
                d['frequency'] = 5
            d['frequency'] = max(d['frequency'], 1)
        elif s == '2':
            d['q'] = line[l+1:r]
            bad = ['/', '\\', '*', '?', ':', '\"', '<', '>', '|']
            name = list(d['q'])
            for i in range(len(name)):
                if name[i] in bad:
                    name[i] = '_'
            d['q'] = ''.join(name)
        elif s == '3':
            d['dateRestrict'] = line[l+1:r].strip()
            valid = ['d', 'w', 'm', 'y']
            if d['dateRestrict'] not in valid:
                d['dateRestrict'] = 'y10'
        elif s == '4':
            d['imgSize'] = line[l+1:r].strip().upper()
            valid = ['HUGE', 'LARGE', 'XLARGE', 'XXLARGE']
            if d['imgSize'] not in valid:
                d['imgSize'] = 'LARGE'
        elif s == '5':
            try:
                d['fetchCnt'] = int(line[l+1:r].strip())
            except:
                d['fetchCnt'] = 10
            d['fetchCnt'] = max(1, d['fetchCnt'])
            d['fetchCnt'] = min(100, d['fetchCnt'])
        elif s == '6':
            try:
                d['mode'] = int(line[l+1:r].strip())
            except:
                d['mode'] = 0
            if d['mode'] != 1:
                d['mode'] = 0

    return d


# open config file
def read_config(log):

    config = open('config.txt', 'r')
    lines = config.readlines()
    config.close()
    d = parse(lines)

    if len(d) != 6:
        print("err: invalid config.txt file", file=log, flush=True)
        config = open('backup.txt', 'r')
        lines = config.readlines()
        config.close()
        d = parse(lines)  # use backup configuration file
    return d


def main():

    # create file for logging errors
    log = open('log.txt', 'w')
    log.truncate(0)
    print("Log Start\n", file=log, flush=True)

    data_path = os.getcwd() + "\\data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    d = read_config(log)
    freq = d['frequency']
    prev_query = d['q']

    # Create a Thread object responsible for downloading images
    downloader_thread = Thread()

    # A argument to the downloader thread to stop it's execution prematurely
    stop = [False]

    while True:

        d = read_config(log)
        freq = d['frequency']

        # Trigger download when user has entered a new query
        if d['q'] != prev_query:

            # Stop previously running downloader thread, if any, safely
            if downloader_thread.is_alive():
                # acquiring lock here is not needed
                stop[0] = True
                downloader_thread.join()
                stop[0] = False

            prev_query = d['q']
            downloader_thread = Thread(target=get_images.fetch,
                                       args=(d, log, stop))
            downloader_thread.start()

        # Change wallpaer
        setter.set_wallpaper(d['q'], d['mode'], log)

        # Put the "main" thread to sleep for freq seconds
        time.sleep(freq)


if __name__ == "__main__":
    main()
