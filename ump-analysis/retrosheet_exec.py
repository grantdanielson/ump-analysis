from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import os


def download_and_unzip(url, extract_to='./retrosheet'):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


def a():
    return


os.system("ls -l")