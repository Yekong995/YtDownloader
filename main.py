from youtube_dl import YoutubeDL
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QFileDialog
from sys import argv, exit
from os import remove
from os.path import exists
from gui import Ui_MainWindow
from platform import system
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon
from re import compile
import configparser

user_os = system()

def rename_file(source:str, name:str):
    source_file = source
    ext = source.split(".")[-1]
    new_name = name + "." + ext
    new_name = source.replace(source.split("\\")[-1], new_name).replace("|", "")
    with open(source_file, "rb") as f:
        try:
            with open(new_name, "wb") as f2:
                f2.write(f.read())
                f2.close()
        except Exception as e:
            return
        f.close()
    remove(source_file)

class Background(QThread):

    def __init__(self, url, ytdl_opts, main_ui, search=False) -> None:
        QThread.__init__(self)
        self.ytdl_opts = ytdl_opts
        self.url = url
        self.search = search
        self.ui = main_ui

    def UpdateProgressBar(self, d):
        if d['status'] == 'finished':
            self.ui.progressBar.setValue(100)
        elif d['status'] == 'downloading':
            self.ui.progressBar.setValue(round(float(d['_percent_str'].replace('%', ''))))

    def run(self) -> None:
        self.ytdl_opts['progress_hooks'] = [self.UpdateProgressBar]
        ydl = YoutubeDL(self.ytdl_opts)
        if self.search:
            info = YoutubeDL(self.ytdl_opts).extract_info(self.url, download=False)
            text = info['entries'][0]['webpage_url']
            name = info['entries'][0]['title']
            file_name = ydl.prepare_filename(info['entries'][0])
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

        if exists("config.ini"):
            config = configparser.ConfigParser()
            config.read("config.ini")
            self.path = config['SETTINGS']['path']
        else:
            with open("config.ini", "w") as f:
                if user_os == "Windows":
                    from os import environ
                    self.path = environ["USERPROFILE"] + '\\Downloads\\'
                elif user_os == "Linux":
                    from os.path import expanduser
                    self.path = expanduser("~") + '/Downloads/'
                else:
                    from os.path import expanduser
                    self.path = expanduser("~") + '/Downloads/'
                    QMessageBox.warning(self, "Warning", "Cannot determine OS, defaulting to Linux")
                f.write("[SETTINGS]\npath=" + self.path)
                f.close()

        self.ui.path.setText(self.path)
        self.ui.path.setDisabled(True)

        self.path += '%(title)s.%(ext)s'
        self.ytdl_format_options['outtmpl'] = self.path

    def download(self):
        audio = self.ui.audioCheck.isChecked()
        text_ls = self.ui.text.text()
        url_regex = compile(r'(https?://\S+)')
        if text_ls == "":
            QMessageBox.critical(self, "Error", "Please input a link")
        elif not url_regex.match(text_ls):
            QMessageBox.critical(self, "Error", "Please input a valid link")
        else:
            if audio:
                self.ytdl_format_options['format'] = 'bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp3'
            else:
                self.ytdl_format_options['format'] = 'bestvideo+bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp4'

            self.worker = Background(text_ls, self.ytdl_format_options, self.ui)

            QMessageBox.information(self, "Download", "Download started")
            self.worker.start()
            self.ui.text.setDisabled(True)
            self.ui.audioCheck.setDisabled(True)
            self.ui.downBtn.setDisabled(True)
            self.ui.dsBtn.setDisabled(True)
            self.worker.finished.connect(self.download_finished)

    def search(self):
        audio = self.ui.audioCheck.isChecked()
        text_ls = self.ui.text.text()
        if text_ls == "":
            QMessageBox.critical(self, "Error", "Please input a string")
        else:
            if audio:
                self.ytdl_format_options['format'] = 'bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp3'
            else:
                self.ytdl_format_options['format'] = 'bestvideo+bestaudio/best'
                self.ytdl_format_options['merge_output_format'] = 'mp4'

            self.worker = Background(text_ls, self.ytdl_format_options, self.ui, search=True)

            QMessageBox.information(self, "Download", "Download started")
            self.worker.start()
            self.ui.text.setDisabled(True)
            self.ui.audioCheck.setDisabled(True)
            self.ui.downBtn.setDisabled(True)
            self.ui.dsBtn.setDisabled(True)
            self.worker.finished.connect(self.download_finished)

    def download_finished(self):
        self.ui.progressBar.setValue(100)
        QMessageBox.information(self, "Download", "Download completed")
        self.ui.text.setDisabled(False)
        self.ui.audioCheck.setDisabled(False)
        self.ui.downBtn.setDisabled(False)
        self.ui.dsBtn.setDisabled(False)
        self.ui.progressBar.setValue(0)

    def change_path(self):
        self.path = QFileDialog.getExistingDirectory(self, "Select Directory", self.path)
        self.path = self.path.replace("/", "\\")
        self.ui.path.setText(self.path)

        config = configparser.ConfigParser()
        config.read("config.ini")
        config['SETTINGS']['path'] = self.path
        with open("config.ini", "w") as f:
            config.write(f)
        
        QMessageBox.information(self, "Path", "Path changed to " + self.path)

        self.path += '%(title)s.%(ext)s'
        self.ytdl_format_options['outtmpl'] = self.path


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainUI()
    window.show()
    exit(app.exec_())
