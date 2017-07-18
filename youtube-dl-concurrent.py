import asyncio
import sys
import youtube_dl

ydl_opts = {
    'format': 'mp4',
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
