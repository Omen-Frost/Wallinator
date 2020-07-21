import requests
import time
import os
from googleapiclient.discovery import build


def fetch(d, dl_path, log):

    # hide this
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


    for url in urls:
        filename = url.split('/')[-1]
        j = filename.lower().find('.jpg')
        if j==-1 :
            continue
        filename = filename[0:j+4]
        print("downloaded:" + filename,file=log, flush=True)

        try :
            response = requests.get(url, timeout=7) # download url content
        except Exception as e:
            print(e, file=log, flush=True)
            continue
        if response.status_code == 200: # Successful download
            open(os.path.join(dl_path, filename), 'wb').write(response.content) # write image

    time.sleep(0.5)
