from youtube_dl import YoutubeDL
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from sys import argv, exit
from gui import Ui_MainWindow
from pathlib import Path
from platform import system
from PyQt5.QtCore import QThread

save_path = str(Path.home() / "Downloads")
user_os = system()

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
            ydl.download([text])
        else:
            ydl.download([self.url])
    

class MainUI(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("YtDownloader")
        self.ytdl_format_options = {
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
        if user_os == "Windows":
            self.ytdl_format_options['outtmpl'] = save_path + '\\' + '%(title)s.%(ext)s'
        elif user_os == "Linux":
            self.ytdl_format_options['outtmpl'] = save_path + '/' + '%(title)s.%(ext)s'
        else:
            self.ytdl_format_options['outtmpl'] = save_path + '/' + '%(title)s.%(ext)s'
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
            self.worker.finished.connect(self.download_finished)

    def download_finished(self):
        self.ui.progressBar.setValue(100)
        QMessageBox.information(self, "Download", "Download completed")
        self.ui.progressBar.setValue(0)


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainUI()
    window.show()
    exit(app.exec_())
