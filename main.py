from youtube_dl import YoutubeDL
from loguru import logger as log
from pathlib import Path
import asyncio
import platform

save_path = str(Path.home() / "Downloads")
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': save_path + '\\' + '%(title)s.%(ext)s',
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
    ytdl_format_options['outtmpl'] = save_path + '\\' + '%(title)s.%(ext)s'
elif platform.system() == "Linux":
    ytdl_format_options['outtmpl'] = save_path + '/' + '%(title)s.%(ext)s'
else:
    log.warning('Cannot determine OS, defaulting to Linux')
    ytdl_format_options['outtmpl'] = save_path + '/' + '%(title)s.%(ext)s'

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
        log.info(f"Downloading {filename}")
        if Path(filename).exists():
            log.warning(f"File {filename} already exists")
            return
        else:
            ytdl.download([url])
        log.info(f"Done downloading {filename}")

async def main():
    while True:
        print("""
[1] Download music
[2] Download video
[Q] Quit
        """)
        choice = input("Enter the option: ")
        if choice == "1":
            link = input("Enter the link: ")
            await download(link, audio_only=True)
        elif choice == "2":
            link = input("Enter the link: ")
            await download(link)
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
