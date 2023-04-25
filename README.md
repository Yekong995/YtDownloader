# YtDownloader

> ** Library `youtube-dl` have problem and can't use **

- [Installation (Terminal)](#Installation-Terminal)
- [Installation (Gui)](#Installation-Gui)

## Installation (Terminal)

- [Linux](#Linux)

- [Windows](#Windows)

### Linux

Requirements:

| Tool    | Command                           |
| ------- | --------------------------------- |
| Python3 | `sudo apt install python3 -y`     |
| pip3    | `sudo apt install python3-pip -y` |



Package:

| Package    | Command |
| ---------- | --------------- |
| youtube-dl | `pip3 install --upgrade youtube-dl` |
| loguru     | `pip3 install --upgrade loguru` |



Run:

```bash
git clone https://github.com/Yekong995/YtDownloader.git
cd YtDownloader
python3 main.py
```

### Windows

Requirements:

| Tool             | Link                                                  |
| ---------------- | ----------------------------------------------------- |
| Python3.8+ & pip | [Link to download](https://www.python.org/downloads/) |

Please tick this option before continue install python:

![install_option](Image/py_install.png)

After tick `Add python.exe to PATH` press `Install Now` or `Customize installation`

> **NOTE: If you chose `Customize installation` make sure you have install pip**



Package:

| Package    | Command                            |
| ---------- | ---------------------------------- |
| youtube-dl | `pip install --upgrade youtube-dl` |
| loguru     | `pip install --upgrade loguru`     |



Run:

```bash
git clone https://github.com/Yekong995/YtDownloader.git
cd YtDownloader
python main.py
```

or

```bash
git clone https://github.com/Yekong995/YtDownloader.git
cd YtDownloader
py main.py
```

## Installation (Gui)

### Windows

Requirements:

You can refer to [here](#Installation-terminal) (Requirements)



Package:

You can also refer to [here](#Installation-Terminal) (Package)

> **NOTE: Package `loguru` can ignore**



New Package:

| Package | Command                       |
| ------- | ----------------------------- |
| PyQt5   | `pip install --upgrade pyqt5` |



Run:

```bash	
git clone https://github.com/Yekong995/YtDownloader.git
cd YtDownloader
python main(pyqt).py
```

or

```bash
git clone https://github.com/Yekong995/YtDownloader.git
cd YtDownloader
py main(pyqt).py
```

