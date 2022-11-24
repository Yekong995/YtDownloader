from youtube_dl import YoutubeDL
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from sys import argv, exit
from re import sub, compile
from os import remove
from gui import Ui_MainWindow
from platform import system
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon

user_os = system()

def rename_file(source:str, name:str):
    source_file = source
    new_name = source.split("\\")[-1]
    new_name = new_name.replace(new_name.split(".")[0], name)
    new_name = sub(compile(r"[<>:\"/\\|?*]"), "", new_name)
    new_name = new_name.replace(" ", "_")
    new_name = source.replace(source.split("\\")[-1], new_name)
    with open(source_file, "rb") as f:
        with open(new_name, "wb") as f2:
            f2.write(f.read())
            f2.close()
        f.close()
    remove(source_file)

class Background(QThread):

    def __init__(self, url, ytdl_opts, search=False) -> None:
        QThread.__init__(self)
        self.ytdl_opts = ytdl_opts
        self.url = url
        self.search = search

    def run(self) -> None:
        ydl = YoutubeDL(self.ytdl_opts)
        if self.search:
            info = YoutubeDL(self.ytdl_opts).extract_info(self.url, download=False)
            text = info['entries'][0]['webpage_url']
            name = info['entries'][0]['title']
            file_name = ydl.prepare_filename(info)
            ydl.download([text])
            rename_file(file_name, name)
        else:
            info = YoutubeDL(self.ytdl_opts).extract_info(self.url, download=False)
            file_name = ydl.prepare_filename(info)
            ydl.download([self.url])
            rename_file(file_name, info['title'])


class MainUI(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("YtDownloader")
        self.setFixedSize(self.size())
        self.setWindowIcon(QIcon("App.ico"))
        self.ytdl_format_options = {
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
            self.ytdl_format_options['outtmpl'] = environ["USERPROFILE"] + '\\Downloads\\' + '%(title)s.%(ext)s'
        elif user_os == "Linux":
            from os.path import expanduser
            self.ytdl_format_options['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'
        else:
            from os.path import expanduser
            self.ytdl_format_options['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'
            QMessageBox.warning(self, "Warning", "Cannot determine OS, defaulting to Linux")

    def download(self):
        audio = self.ui.audioCheck.isChecked()
        text_ls = self.ui.text.text()
        if text_ls == "":
            QMessageBox.critical(self, "Error", "Please input a link or string")
        else:
            self.ui.progressBar.setValue(5)
            if audio:
                self.ytdl_format_options['format'] = 'bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp3'
            else:
                self.ytdl_format_options['format'] = 'bestvideo+bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp4'
            self.worker = Background(text_ls, self.ytdl_format_options)
            self.ui.progressBar.setValue(10)
            QMessageBox.information(self, "Download", "Download started")
            self.worker.start()
            self.ui.progressBar.setValue(15)
            self.ui.text.setDisabled(True)
            self.ui.audioCheck.setDisabled(True)
            self.ui.downBtn.setDisabled(True)
            self.ui.dsBtn.setDisabled(True)
            self.ui.progressBar.setValue(20)
            self.worker.finished.connect(self.download_finished)

    def search(self):
        audio = self.ui.audioCheck.isChecked()
        text_ls = self.ui.text.text()
        if text_ls == "":
            QMessageBox.critical(self, "Error", "Please input a link or string")
        else:
            self.ui.progressBar.setValue(5)
            if audio:
                self.ytdl_format_options['format'] = 'bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp3'
            else:
                self.ytdl_format_options['format'] = 'bestvideo+bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp4'
            self.worker = Background(text_ls, self.ytdl_format_options, search=True)
            self.ui.progressBar.setValue(10)
            QMessageBox.information(self, "Download", "Download started")
            self.worker.start()
            self.ui.progressBar.setValue(15)
            self.ui.text.setDisabled(True)
            self.ui.audioCheck.setDisabled(True)
            self.ui.downBtn.setDisabled(True)
            self.ui.dsBtn.setDisabled(True)
            self.ui.progressBar.setValue(20)
            self.worker.finished.connect(self.download_finished)

    def download_finished(self):
        self.ui.progressBar.setValue(100)
        QMessageBox.information(self, "Download", "Download completed")
        self.ui.text.setDisabled(False)
        self.ui.audioCheck.setDisabled(False)
        self.ui.downBtn.setDisabled(False)
        self.ui.dsBtn.setDisabled(False)
        self.ui.progressBar.setValue(0)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainUI()
    window.show()
    exit(app.exec_())
