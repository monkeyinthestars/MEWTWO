import random
import threading

from download_manager import get_url
from generate_matchup_table import get_decklist_url_per_player

RK9_URL = "https://rk9.gg/pairings/LA01mwu6ugCwMEJxWT2H" # LAIC
NB_CONCURENCY = 10

def download_urls(url_list):
    for url in url_list:
        get_url(url)

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

if __name__ == "__main__":
    decklist_url_per_player = get_decklist_url_per_player(RK9_URL)
    url_list = list(decklist_url_per_player.values())
    random.shuffle(url_list) # Shuffling in case some url have already been downloaded

    url_list_split = split(url_list, NB_CONCURENCY)
    thread_list = []
    for url_list in url_list_split:
        thread = threading.Thread(target=download_urls, args=[url_list])
        thread.start()
        thread_list.append(thread)

    for thread in thread_list:
        thread.join()

    print("Congratulations!! You downloaded your tournament :)")

