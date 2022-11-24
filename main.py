from youtube_dl import YoutubeDL
from pathlib import Path
from loguru import logger as log
from os import remove
from re import sub, compile
import asyncio
import platform

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # bind to ipv4 since ipv6 addresses cause issues sometimes
    'merge_output_format': 'mp3'
}

if platform.system() == "Windows":
    from os import environ
    ytdl_format_options['outtmpl'] = environ['USERPROFILE'] + '\\Downloads\\' + '%(title)s.%(ext)s'
elif platform.system() == "Linux":
    from os.path import expanduser
    ytdl_format_options['outtmpl'] = expanduser('~') + '/Downloads/' + '%(title)s.%(ext)s'
else:
    from os.path import expanduser
    log.warning('Cannot determine OS, defaulting to Linux')
    ytdl_format_options['outtmpl'] = expanduser('~') + '/Downloads/' + '%(title)s.%(ext)s'

async def rename_file(source:str, name:str):
    log.info(f"Renaming {source} to {name}")
    source_file = source
    new_name = source.split("\\")[-1]
    new_name = new_name.replace(new_name.split(".")[0], name)
    new_name = source.replace(source.split("\\")[-1], new_name)
    with open(source_file, 'rb') as f:
        with open(new_name, 'wb') as f1:
            f1.write(f.read())
            f1.close()
        f.close()
    remove(source_file)

async def download(url, audio_only=False):
    if url == "":
        log.critical("No link provided")
        return
    else:
        if audio_only:
            ytdl_format_options['format'] = 'bestaudio/best'
            ytdl_format_options['merge_output_format'] = 'mp3'
        else:
            ytdl_format_options['format'] = 'bestvideo+bestaudio/best'
            ytdl_format_options['merge_output_format'] = 'mp4'
        ytdl = YoutubeDL(ytdl_format_options)
        info = ytdl.extract_info(url, download=False)
        filename = ytdl.prepare_filename(info)
        name = sub(compile(r"[^\w\s]"), "", info['title'])
        log.info(f"Downloading {filename}")
        if Path(filename).exists():
            log.warning(f"File {filename} already exists")
            return
        else:
            ytdl.download([url])
        log.info(f"Done downloading {filename}")
        await rename_file(filename, name)
        log.info(f"Done renaming {filename}")

async def search(name, mode='m'):
    ytdl = YoutubeDL(ytdl_format_options)
    info = ytdl.extract_info(f"ytsearch:{name}", download=False)['entries'][0]
    log.info(f"Found: {info['title']}")
    if mode == 'm':
        await download(info['webpage_url'], audio_only=True)
    elif mode == 'v':
        await download(info['webpage_url'])
    else:
        log.critical("Invalid mode")
        return

async def main():
    while True:
        print("""
[1] Download music
[2] Download video
[3] Search & Download
[Q] Quit
        """)
        choice = input("Enter the option: ")
        if choice == "1":
            link = input("Enter the link: ")
            await download(link, audio_only=True)
        elif choice == "2":
            link = input("Enter the link: ")
            await download(link)
        elif choice == "3":
            name = input("Enter the name: ")
            m3orm4 = input("Do you want to download music or video? (m/v): ")
            await search(name, mode=m3orm4)
        elif choice == "Q" or choice == "q":
            loop.stop()
            break
        else:
            log.critical("Invalid option")
            continue

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(main(), loop=loop)
    loop.run_until_complete(future)
