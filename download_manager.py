"""
Goal: Avoid redownloading static pages by caching them on disk.
"""

import os
import time

import requests
from bs4 import BeautifulSoup
from mlp.bettercoding import print_del

only_useragent_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:62.0) Gecko/20100101 Firefox/80.0",
}


def get_page_from_url(url: str, max_retries: int = 100) -> requests.Response:
    """
    Downloads a web page from the given URL with retry logic.

    Args:
        url (str): The URL of the web page to download.
        max_retries (int): The maximum number of retries.

    Returns:
        requests.Response: The HTTP response object containing the web page content.
    """
    print(f"Downloading {url}...")
    nb_retry = 1
    while True:
        try:
            page = requests.get(url, headers=only_useragent_headers, timeout=120)
            return page
        except requests.exceptions.RequestException as e:
            if nb_retry >= max_retries:
                raise e
            if nb_retry > 1:
                print_del()
            print(f"{e} | Retrying for the {nb_retry} time")
            time.sleep(5)
        nb_retry += 1


def get_url(url: str) -> bytes:
    """
    Retrieves the content of a URL. If the content is cached locally, loads it from disk.
    Otherwise, downloads the content and caches it.

    Args:
        url (str): The URL to retrieve content from.

    Returns:
        bytes: The binary content of the URL.
    """
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


def get_soup_from_url(url: str) -> BeautifulSoup:
    """
    Retrieves a BeautifulSoup object parsed from the content of a URL.

    Args:
        url (str): The URL to retrieve and parse.

    Returns:
        BeautifulSoup: A BeautifulSoup object representing the parsed HTML content.
    """
    content = get_url(url)
    soup = BeautifulSoup(content, "html.parser")
    return soup
