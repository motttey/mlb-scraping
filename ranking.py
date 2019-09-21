from __future__ import unicode_literals

import numpy as np
import sys as sys
import json

def main():
    f = open('out_batter.json', 'r', encoding="utf-8")

    jsonData = json.load(f)
    time_array = jsonData['time_array']

    for val in time_array:
        keys = list(val)
        print(keys[0])
        time_val = val[keys[0]]

        time_val_sorted = sorted(time_val, key=lambda x: x["Btype"])
        time_val_sorted_row20 = time_val_sorted[0:19]

        for player in time_val_sorted_row20:
            print(player["name"].encode("utf-8"))

        print("---")

        time_val_sorted = sorted(time_val, key=lambda x: x["Btype"], reverse=True)
        time_val_sorted_top20 = time_val_sorted[0:19]

        for player in time_val_sorted_top20:
            print(player["name"].encode("utf-8"))

if __name__ == "__main__":
    main()
