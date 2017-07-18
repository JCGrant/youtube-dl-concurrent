import asyncio
import bs4
import os
import requests
import sys
from tqdm import tqdm
import youtube_dl

BASE_DOWNLOAD_DIR = os.getcwd() + '/downloads/'

bars = {}

def update_tqdm(information):
    filename = information['filename']
    downloaded = information['downloaded_bytes']
    total = information['total_bytes'] or information['total_bytes_estimate']
    if downloaded and total:
        if filename not in bars:
            bars[filename] = tqdm(desc=filename[:10], unit='B', unit_scale=True, total=total)
        bar = bars[filename]
        bar.update(downloaded - bar.n)

def download(video_url):
    r = requests.get(video_url)
    soup = bs4.BeautifulSoup(r.text, 'html5lib')
    channel_name = soup.find('div', { 'class': 'yt-user-info'}).text.strip()
    download_dir = BASE_DOWNLOAD_DIR + channel_name + '/'

    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)

    ydl_opts = {
        'format': 'mp4',
        'quiet': True,
        'progress_hooks': [
            update_tqdm,
        ],
        'outtmpl' : download_dir + '%(title)s.%(ext)s'
    }
    ydl = youtube_dl.YoutubeDL(ydl_opts)
    ydl.download([video_url])

if len(sys.argv) < 2:
    print("Usage: python main.py [video-urls-file]")
    exit(1)

filename = sys.argv[1]
with open(filename) as f:
    urls = f.read().strip().split('\n')

loop = asyncio.get_event_loop()
tasks = [
    loop.run_in_executor(
        None,
        download,
        video_url
    ) for video_url in urls
]
loop.run_until_complete(asyncio.wait(tasks))

for bar in bars.values():
    bar.close()
