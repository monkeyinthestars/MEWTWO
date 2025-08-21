import os
import sys

# getting the name of the directory
# where the this file is present.
current = os.path.dirname(os.path.realpath(__file__))

# Getting the parent directory name
# where the current directory is present.
parent = os.path.dirname(current)

# adding the parent directory to 
# the sys.path.
sys.path.append(parent)


from collections import Counter

from mlp.chrono import start_chrono

chrono = start_chrono()
chrono.print_elapsed()
import download_manager

download_manager.save_download_database_soup()

chrono.print_elapsed()
print("Done")

url_list = []
for url, content in download_manager.download_database_soup.items():
    url_list.append(url)


last_part_of_url = [url.split("/")[-1] for url in url_list]

print(f"{len(last_part_of_url) = }")
print("\n".join(last_part_of_url[:10]))

counter_url_last_part = Counter(last_part_of_url)
for last_part_url, occ in counter_url_last_part.items():
    if occ > 1:
        print(last_part_of_url)
