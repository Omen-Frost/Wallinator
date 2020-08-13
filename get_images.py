import requests
import time
import os
from googleapiclient.discovery import build


def fetch(d, log, stop):

    # Change these with your keys
    api_key = "[Your API key]"
    cs_key = "[Your Custom search engine key]"
    

    urls = []
    remaining = d['fetchCnt']
    start_idx = 1

    try:

        # create resource object through which request is sent
        # Custom search engine google
        resource = build("customsearch", 'v1', developerKey=api_key).cse()

        while remaining > 0:

            # create and execute request
            result = resource.list(
                q=d['q'],
                cx=cs_key,
                dateRestrict=d['dateRestrict'],
                searchType='image',
                start=start_idx,
                num=min(remaining, 10),
                fileType='jpg',
                imgSize=d['imgSize'],
                safe='off'
            ).execute()

            for item in result['items']:
                urls.append(item['link'])

            start_idx += 10
            remaining -= 10

    except Exception as e:
        print(e, file=log, flush=True)

    # download directory
    dl_path = os.path.join(os.getcwd() + "\\data", d['q'])
    if not os.path.exists(dl_path):
        os.makedirs(dl_path)

    print('downloading',file=log, flush=True)

    # Download image from each url fetched
    for url in urls:

        filename = url.split('/')[-1]
        filename = filename.lower()
        j = filename.find('.jpg')
        if j==-1 :
            continue
        filename = filename[0:j+4]

        try :
            response = requests.get(url, timeout=3) # download url content
        except Exception as e:
            print(e, file=log, flush=True)
            continue

        if response.status_code == 200: # Successful download
            print("downloaded: " + filename,file=log, flush=True)
            open(os.path.join(dl_path, filename), 'wb').write(response.content) # write image
        
        # check if thread should stop
        if stop[0] :
            print('download interrupted',file=log, flush=True)
            return

    print('download finshed',file=log, flush=True)

