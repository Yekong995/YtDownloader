from youtube_dl import YoutubeDL
from platform import system
import customtkinter
import multiprocessing

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")
root = customtkinter.CTk()

root.title("YtDownloader")
root.geometry("300x250")
root.iconbitmap("App.ico")

user_os = system()

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

if user_os == "Windows":
    from os import environ
    ytdl_format_options['outtmpl'] = environ["USERPROFILE"] + '\\Downloads\\' + '%(title)s.%(ext)s'
elif user_os == "Linux":
    from os.path import expanduser
    ytdl_format_options['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'
else:
    from os.path import expanduser
    ytdl_format_options['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'

def download(url, ytdl_opts, search=False, only_audio=False):
    if only_audio:
        ytdl_opts['format'] = 'bestaudio/best'
        ytdl_opts['merge_output_format'] = 'mp3'
    else:
        ytdl_opts['format'] = 'bestvideo+bestaudio/best'
        ytdl_opts['merge_output_format'] = 'mp4'
    ydl = YoutubeDL(ytdl_opts)
    if search:
        info = YoutubeDL(ytdl_opts).extract_info(url, download=False)
        text = info['entries'][0]['webpage_url']
        ydl.download([text])
    else:
        ydl.download([url])

def thread_download(url, ytdl_opts, search=False):
    if audio_check.get():
        only_audio = True
    else:
        only_audio = False
    p = multiprocessing.Process(target=download, args=(url, ytdl_opts, search, only_audio))
    p.start()

    btn_down_search.configure(state="disabled")
    btn_down_video.configure(state="disabled")
    btn_down_search.configure(text="Downloading...")
    btn_down_video.configure(text="Downloading...")

    while p.is_alive():
        root.update()
    btn_down_search.configure(state="normal")
    btn_down_video.configure(state="normal")
    btn_down_search.configure(text="Search & Download")
    btn_down_video.configure(text="Download")

def change_mode():
    if customtkinter.get_appearance_mode() == "Dark":
        customtkinter.set_appearance_mode("light")
        btn_change_mode.configure(text="Change to Dark Mode")
    else:
        customtkinter.set_appearance_mode("dark")
        btn_change_mode.configure(text="Change to Light Mode")

frame = customtkinter.CTkFrame(root)
frame.pack(expand=True)

title = customtkinter.CTkLabel(frame, text="YtDownloader", text_font=("Arial", 20))
title.grid(row=0, column=0, columnspan=2, pady=10, padx=10)

url_entry = customtkinter.CTkEntry(frame, width=150)
url_entry.grid(row=1, column=0, padx=10)

btn_down_video = customtkinter.CTkButton(frame, text="Download", command=lambda: thread_download(url_entry.get(), ytdl_format_options))
btn_down_video.grid(row=2, column=0, padx=10, pady=10)

btn_down_search = customtkinter.CTkButton(frame, text="Search & Download", command=lambda: thread_download(url_entry.get(), ytdl_format_options, search=True))
btn_down_search.grid(row=3, column=0, padx=10)

audio_check = customtkinter.CTkCheckBox(frame, text="Only Audio")
audio_check.grid(row=4, column=0, padx=10, pady=10)

if customtkinter.get_appearance_mode() == "Dark":
    mode = "Light"
else:
    mode = "Dark"

btn_change_mode = customtkinter.CTkButton(root, text=f"Change to {mode} Mode", command=change_mode)
btn_change_mode.pack(pady=10)

if __name__ == "__main__":
    root.mainloop()
