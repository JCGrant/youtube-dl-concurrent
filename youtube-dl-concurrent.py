import asyncio
import sys
from tqdm import tqdm
import youtube_dl

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

ydl_opts = {
    'format': 'mp4',
    'quiet': True,
    'progress_hooks': [
        update_tqdm,
    ],
}
ydl = youtube_dl.YoutubeDL(ydl_opts)

def download(video_url):
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
