"""
Goal: avoid redownloading static pages
"""

import json
import os
import pickle
from bs4 import BeautifulSoup
import requests
import time

from mlp import print_del



only_useragent_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/80.0",
}


def get_page_from_url(url):
    print(f"Downloading {url}...")
    nb_retry = 1
    while True:
        try:
            page = requests.get(url, headers=only_useragent_headers)
            return page
        except:
            if nb_retry > 1:
                print_del()
            print(f"Retrying for the {nb_retry} time")
            time.sleep(5)
        nb_retry += 1


def get_url(url):
    path_on_disk = url.replace("https://", "").replace("http://", "")
    if os.path.exists(path_on_disk):
        with open(path_on_disk, "rb") as f:
            content = f.read()
        return content
    page = get_page_from_url(url)
    content = page.content
    os.makedirs(os.path.dirname(path_on_disk), exist_ok=True)
    with open(path_on_disk, "wb") as f:
        f.write(content)
    return content


def get_soup_from_url(url):
    content = get_url(url)

    soup = BeautifulSoup(content, "html.parser")
    return soup

from mlp.chrono import start_chrono
def save_download_database():
    print("Saving download database...")
    chrono = start_chrono()
    global download_database
    
    with open("download_database.json", "w") as f:
        json.dump(download_database, f)

    with open("download_database.pkl", "wb") as f:
        pickle.dump(download_database, f)
    
    elapsed = chrono.elapsed_str()
    print(f"download_database saved in {elapsed}")
