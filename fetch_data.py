import requests
import os
from zipfile import ZipFile
import pandas as pd
from config import config


def fetch():
    for element in config:
        
        url = element['url']
        local_path = element['local_path']
        # Inspired by https://365datascience.com/tutorials/python-tutorials/python-requests-package/
        if not os.path.exists(local_path):
            print(f"fetching {url}")
            with requests.get(url, stream = True) as stream:
                with open(local_path, 'wb') as target_file:
                    for chunk in stream.iter_content(chunk_size = 1024 * 1024):
                        target_file.write(chunk)
        else:
            print(f"file {local_path} exists, skipping")

def unpack():
    for element in config:
        local_path = element['local_path']
        unpack_path = element['unpack_path']
        if not os.path.exists(unpack_path):
            print(f"unpacking {local_path}")
            with ZipFile(local_path, 'r') as zipObj:
                zipObj.extractall(unpack_path)
        else:
            print(f"direcory {unpack_path} exists, skipping")

def main():
    fetch()
    unpack()
    print("done")

if __name__ == '__main__':
    main()

