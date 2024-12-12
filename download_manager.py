"""
Goal: avoid redownloading static pages
"""

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



if not os.path.exists("download_database.pkl"):
    download_database = {}
else:
    with open("download_database.pkl", "rb") as f:
        download_database = pickle.load(f)

if not os.path.exists("download_database_soup.pkl"):
    download_database_soup = {}
else:
    with open("download_database_soup.pkl", "rb") as f:
        download_database_soup = pickle.load(f)


def get_url(url):
    global download_database
    if url in download_database.keys():
        return download_database[url]
    page = get_page_from_url(url)
    download_database[url] = page
    return page

def get_soup_from_url(url):
    global download_database_soup
    if url in download_database_soup.keys():
        return download_database_soup[url]
    page = get_page_from_url(url)
    soup = BeautifulSoup(page.content, "html.parser")
    download_database_soup[url] = soup
    
    if len(download_database_soup.keys()) % 10 == 0:
        save_download_database_soup()

    return soup


def save_download_database_soup():
    global download_database_soup
    
    with open("download_database_soup.pkl", "wb") as f:
        pickle.dump(download_database_soup, f, protocol=5)