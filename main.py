from os import listdir
from os.path import isfile, join
import requests
import time
import tkinter as tk
from tkinter import filedialog

API_KEY = ""
URL = "https://osu.ppy.sh/api/get_beatmaps"
NAME = "Collection"


def open_window():
    set_ids = []
    root = tk.Tk()
    root.withdraw()
    mypath = filedialog.askdirectory()
    mapslist = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    for mapz in mapslist:
        set_ids.append(mapz.split()[0])
    return set_ids


def get_map_ids(api_key, url, set_ids):
    maps_list = []
    for setid in set_ids:
        payload = {
            'k': api_key,
            's': setid,
            'limit': 10,
        }
        map_ids = requests.get(url, params=payload).json()
        time.sleep(1)
        for map_id in map_ids:
            if float(map_id["difficultyrating"]) >= 5:
                maps_list.append(map_id["beatmap_id"])
    return maps_list


def get_md5_hashes(api_key, url, maps_list):
    md5_hashes = []
    for mapid in maps_list:
        payload = {
            'k': api_key,
            'b': mapid,
            'limit': 100,
        }
        req = requests.get(url, params=payload).json()
        time.sleep(1)
        md5_hashes.append(req[0]["file_md5"])
    return md5_hashes


def save_collection_to_file(md5_hashes, name):
    with open("Collection.db", "wb") as collection:
        collection.write(b"\x00\x00\x00\x00" +
                         (1).to_bytes(4, "little") +
                         b"\x0b" +
                         len(name).to_bytes(1, "little") +
                         name.encode() +
                         len(md5_hashes).to_bytes(4, "little"))
        for md5_hash in md5_hashes:
            collection.write(b"\x0b " + md5_hash.encode())


if __name__ == "__main__":
    sids = open_window()
    mids = get_map_ids(API_KEY, URL, sids)
    mhashes = get_md5_hashes(API_KEY, URL, mids)
    save_collection_to_file(mhashes, NAME)
