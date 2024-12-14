"""
Tournament Data Downloader Module

This module automates downloading tournament-related data from URLs. It retrieves decklist URLs for players
from an external pairing system and utilizes multithreading to download data efficiently.

Constants:
    RK9_URL (str): URL to fetch tournament pairings and decklist information.
    NB_CONCURRENCY (int): Number of concurrent threads for downloading.

Functions:
    download_urls(url_list: List[str]) -> None:
        Downloads content from a list of URLs using the get_url function.

    split(lst: List[str], parts: int) -> List[List[str]]:
        Divides a list into nearly equal-sized parts for balanced workload distribution.

Execution:
    When executed directly, the script will download the tournament associated with the RK9_URL constant.
"""

import random
import threading
from typing import List

from download_manager import get_url
from generate_matchup_table import get_decklist_url_per_player

RK9_URL = "https://rk9.gg/pairings/WCS01mIMYt8if4wVuaO0" # Worlds
NB_CONCURENCY = 10


def download_urls(url_list: List[str]) -> None:
    """
    Ensure a list of URLs is downloaded by calling the `get_url` function.

    Args:
        url_list (List[str]): A list of URLs to download.
    """
    for url in url_list:
        get_url(url)

def split(lst: List[str], parts: int) -> List[List[str]]:
    """
    Splits a list into a specified number of nearly equal parts.

    Args:
        lst (List[str]): The list to split.
        parts (int): The number of parts to split the list into.

    Returns:
        List[List[str]]: A list of sublists, where each sublist is a chunk of the original list.
    """
    if parts <= 0:
        raise ValueError("The number of parts must be greater than 0.")

    chunk_size, remainder = divmod(len(lst), parts)
    results = []

    start = 0
    for _ in range(parts):
        end = start + chunk_size
        results.append(lst[start:end])
        start = end

    if remainder > 0:
        results[-1] += lst[-remainder:]

    return results


if __name__ == "__main__":
    decklist_url_per_player = get_decklist_url_per_player(RK9_URL)
    url_chunk = list(decklist_url_per_player.values())
    random.shuffle(url_chunk) # Shuffling in case some url have already been downloaded

    url_list_split = split(url_chunk, NB_CONCURENCY)
    thread_list = []
    for url_chunk in url_list_split:
        thread = threading.Thread(target=download_urls, args=[url_chunk])
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    print("Congratulations!! You downloaded your tournament :)")
