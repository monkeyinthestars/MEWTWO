"""
Goal: avoid redownloading static pages
"""

import json
import os
import pickle
import time

import requests
from bs4 import BeautifulSoup
from mlp import print_del
from mlp.chrono import start_chrono

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
    path_on_disk = path_on_disk.replace("?", "__QUESTIONMARKTOKEN__")
    path_on_disk = path_on_disk.replace("&", "__AMPTOKEN__")
    path_on_disk = path_on_disk.replace("=", "__EQTOKEN__")
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

