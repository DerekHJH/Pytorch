# 爬虫代码, 只能run一次，千万不要再继续，持续时间太久
import requests
from bs4 import BeautifulSoup
import os
import traceback

kv = {'user-agent': 'Mozilla/5.0'}

def download(url, filename):
    if os.path.exists(filename):
        print('file exists!')
        return
    try:
        r = requests.get(url, stream = True, timeout = 60, headers = kv)
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size = 1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    f.flush()
        return filename
    except KeyboardInterrupt:
        if os.path.exists(filename):
            os.remove(filename)
        raise KeyboardInterrupt
    except Exception:
        traceback.print_exc()
        if os.path.exists(filename):
            os.remove(filename)


if os.path.exists('data/anime') is False:
    os.makedirs('data/anime')

start = 820
end = 8000
for i in range(start, end + 1):
    url = 'http://konachan.net/post?page=%d&tags=' % i
    soup = BeautifulSoup(requests.get(url, headers = kv).text, 'html.parser')
    for img in soup.find_all('img', class_ = "preview"):
        target_url = img['src']
        filename = os.path.join('data/anime', target_url.split('/')[-1])
        download(target_url, filename)
    print('%d / %d' % (i, end))