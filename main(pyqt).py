from youtube_dl import YoutubeDL
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from sys import argv, exit
from os import remove
from gui import Ui_MainWindow
from platform import system
from PyQt5.QtCore import QThread
from PyQt5.QtGui import QIcon

user_os = system()

def rename_file(source:str, name:str):
    source_file = source
    ext = source.split(".")[-1]
    new_name = name + "." + ext
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
        self.ytdl_format_options_login = {
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
            'merge_output_format': 'mp3',
            'username': 'username',
            'password': 'password'
        }
        if user_os == "Windows":
            from os import environ
            self.ytdl_format_options['outtmpl'] = environ["USERPROFILE"] + '\\Downloads\\' + '%(title)s.%(ext)s'
            self.ytdl_format_options_login['outtmpl'] = environ["USERPROFILE"] + '\\Downloads\\' + '%(title)s.%(ext)s'
        elif user_os == "Linux":
            from os.path import expanduser
            self.ytdl_format_options['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'
            self.ytdl_format_options_login['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'
        else:
            from os.path import expanduser
            self.ytdl_format_options['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'
            self.ytdl_format_options_login['outtmpl'] = expanduser("~") + '/Downloads/' + '%(title)s.%(ext)s'
            QMessageBox.warning(self, "Warning", "Cannot determine OS, defaulting to Linux")

    def download(self):
        audio = self.ui.audioCheck.isChecked()
        text_ls = self.ui.text.text()
        if text_ls == "":
            QMessageBox.critical(self, "Error", "Please input a link or string")
        else:
            self.ui.progressBar.setValue(5)
            if audio:
                if self.check_login():
                    self.ytdl_format_options_login['format'] = 'bestaudio/best'
                    self.ytdl_format_options_login['merge_output_format'] = 'mp3'
                    self.ytdl_format_options_login['username'] = self.ui.mail.text()
                    self.ytdl_format_options_login['password'] = self.ui.password.text()
                else:
                    self.ytdl_format_options['format'] = 'bestaudio/best'
                    self.ytdl_format_options['merge_output_format'] = 'mp3'
            else:
                if self.check_login():
                    self.ytdl_format_options_login['format'] = 'bestvideo+bestaudio/best'
                    self.ytdl_format_options_login['merge_output_format'] = 'mp4'
                    self.ytdl_format_options_login['username'] = self.ui.mail.text()
                    self.ytdl_format_options_login['password'] = self.ui.password.text()
                else:
                    self.ytdl_format_options['format'] = 'bestvideo+bestaudio/best'
                    self.ytdl_format_options['merge_output_format'] = 'mp4'
            if self.check_login():
                self.worker = Background(text_ls, self.ytdl_format_options_login)
            else:
                self.worker = Background(text_ls, self.ytdl_format_options)
            self.ui.progressBar.setValue(10)
            QMessageBox.information(self, "Download", "Download started")
            self.worker.start()
            self.ui.progressBar.setValue(15)
            self.ui.text.setDisabled(True)
            self.ui.audioCheck.setDisabled(True)
            self.ui.downBtn.setDisabled(True)
            self.ui.dsBtn.setDisabled(True)
            self.ui.mail.setDisabled(True)
            self.ui.password.setDisabled(True)
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
                if self.check_login():
                    self.ytdl_format_options_login['format'] = 'bestaudio/best'
                    self.ytdl_format_options_login['merge_output_format'] = 'mp3'
                    self.ytdl_format_options_login['username'] = self.ui.mail.text()
                    self.ytdl_format_options_login['password'] = self.ui.password.text()
                else:
                    self.ytdl_format_options['format'] = 'bestaudio/best'
                    self.ytdl_format_options['merge_output_format'] = 'mp3'
            else:
                if self.check_login():
                    self.ytdl_format_options_login['format'] = 'bestvideo+bestaudio/best'
                    self.ytdl_format_options_login['merge_output_format'] = 'mp4'
                    self.ytdl_format_options_login['username'] = self.ui.mail.text()
                    self.ytdl_format_options_login['password'] = self.ui.password.text()
                else:
                    self.ytdl_format_options['format'] = 'bestvideo+bestaudio/best'
                    self.ytdl_format_options['merge_output_format'] = 'mp4'
            if self.check_login():
                self.worker = Background(text_ls, self.ytdl_format_options_login, search=True)
            else:
                self.worker = Background(text_ls, self.ytdl_format_options, search=True)
            self.ui.progressBar.setValue(10)
            QMessageBox.information(self, "Download", "Download started")
            self.worker.start()
            self.ui.progressBar.setValue(15)
            self.ui.text.setDisabled(True)
            self.ui.audioCheck.setDisabled(True)
            self.ui.downBtn.setDisabled(True)
            self.ui.dsBtn.setDisabled(True)
            self.ui.mail.setDisabled(True)
            self.ui.password.setDisabled(True)
            self.ui.progressBar.setValue(20)
            self.worker.finished.connect(self.download_finished)

    def download_finished(self):
        self.ui.progressBar.setValue(100)
        QMessageBox.information(self, "Download", "Download completed")
        self.ui.text.setDisabled(False)
        self.ui.audioCheck.setDisabled(False)
        self.ui.downBtn.setDisabled(False)
        self.ui.dsBtn.setDisabled(False)
        self.ui.mail.setDisabled(False)
        self.ui.password.setDisabled(False)
        self.ui.progressBar.setValue(0)

    def check_login(self):
        mail = self.ui.mail.text()
        password = self.ui.password.text()
        if mail == "" or password == "":
            return False
        else:
            return True


if __name__ == "__main__":
    app = QApplication(argv)
    window = MainUI()
    window.show()
    exit(app.exec_())
