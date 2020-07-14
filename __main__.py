import setter
import os
import time
import get_images

# parses config file to read settings and set search parameters
def parse(lines):
    d = {}
    for line in lines:
        s = line[0]
        l = line.find('(')
        r = line.rfind(')')
        if l>=r :
            continue
        if s == '1':
            try:
                d['frequency'] = int(line[l+1:r].strip())
            except:
                d['frequency'] = 5
            d['frequency'] = max(d['frequency'], 1)
        elif s == '2':
            d['q'] = line[l+1:r]
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

    return d

# open config file 
def read_config(log):

    config = open('config.txt', 'r')
    lines = config.readlines()
    config.close()
    d = parse(lines)

    if len(d) != 5:
        print("err: invalid config.txt file", file=log)
        config = open('backup.txt', 'r')
        lines = config.readlines()
        config.close()
        d = parse(lines)  # use backup configuration file
    return d


def main():

    # create file for logging errors
    log = open('log.txt', 'w')
    log.truncate(0)
    print("Log Start\n", file=log)

    data_path = os.getcwd() + "\\data"
    if not os.path.exists(data_path):
        os.makedirs(data_path)

    new_path = os.getcwd() + "\\new"
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    d = read_config(log)
    freq = d['frequency']
    prev_query = d['q']
    use_path = data_path

    while True:

        d = read_config(log)

        freq = d['frequency']

        if d['q'] == prev_query:

            # set a random image as wallpaper from the specified path
            p = setter.set_wallpaper(
                use_path, (use_path != data_path), data_path)
            if p == -1:
                print("err: set failed", file=log)
            elif p == 0:
                print("no files left, switch to data", file=log)
                use_path = data_path
            else:
                print("set", file=log)

            # Put the process to sleep for freq seconds
            time.sleep(max(freq, 1)) 

        else:

            use_path = new_path
            prev_query = d['q']
            # prevent keyboard interrupt here
            print('downloading',file=log)
            get_images.fetch(d, new_path, log)
            print('download finshed',file=log)


if __name__ == "__main__":
    main()
