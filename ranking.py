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
            tb = int(player["single_hits"]) + 2* int(player["two_base"]) + 3 * int(player["three_base"]) + 4 * int(player["home_runs"])

            obp_1 = int(player["single_hits"]) + int(player["two_base"]) + int(player["three_base"]) + int(player["home_runs"]) + int(player["BB"]) + int(player["HBP"])
            obp_2 = int(player["PA"])
            obp = obp_1/obp_2 if (player["PA"] > 0) else 0

            print(str(player["name"].encode("utf-8")) + ": Number of Game: " +  str(player["Number of Game"]) + ", Btype: "+ str("{:.3f}".format(player["Btype"])) + ", TB: " + str(tb) + ", OBP: " + str("{:.3f}".format(obp)))

        print("---")

        time_val_sorted = sorted(time_val, key=lambda x: x["Btype"], reverse=True)
        time_val_sorted_top20 = time_val_sorted[0:19]

        for player in time_val_sorted_top20:
            tb = int(player["single_hits"]) + 2* int(player["two_base"]) + 3 * int(player["three_base"]) + 4 * int(player["home_runs"])

            obp_1 = int(player["single_hits"]) + int(player["two_base"]) + int(player["three_base"]) + int(player["home_runs"]) + int(player["BB"]) + int(player["HBP"])
            obp_2 = int(player["PA"])
            obp = obp_1/obp_2 if (player["PA"] > 0) else 0

            print(str(player["name"].encode("utf-8")) + ": Number of Game: " +  str(player["Number of Game"]) + ", Btype: "+ str("{:.3f}".format(player["Btype"])) + ", TB: " + str(tb) + ", OBP: " + str("{:.3f}".format(obp)))

if __name__ == "__main__":
    main()
