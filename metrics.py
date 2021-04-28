from __future__ import unicode_literals

import numpy as np
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import spearmanr, kendalltau
from sklearn.metrics import precision_score, recall_score

def get_sorted(sortKey, idx, time_array, reverse=False):
    keys = list(time_array[idx])
    time_val = time_array[idx][keys[0]]

    for player in time_val:
        player["TB"] = int(player["single_hits"]) + 2* int(player["two_base"]) + 3 * int(player["three_base"]) + 4 * int(player["home_runs"])

        obp_1 = int(player["single_hits"]) + int(player["two_base"]) + int(player["three_base"]) + int(player["home_runs"]) + int(player["BB"]) + int(player["HBP"])
        obp_2 = int(player["PA"])

        player["AB"] = 	player["PA"] - player["SH"] - player["SF"] - player["BB"] - player["HBP"]
        player["OBP"] = obp_1/obp_2 if (player["PA"] > 0) else 0
        player["OPS"] = player["OBP"] + player["TB"]/player["AB"] if (player["AB"] > 0) else 0

    return sorted(time_val, key=lambda x: x[sortKey], reverse=reverse)


def get_s_names(first, second):
    s_names_first = [ player['name'] for player in first ]
    s_names_second = [ player['name'] for player in second ]

    return [s_names_first, s_names_second]

def print_jaccard(first, second):
    s_names_first, s_names_second = get_s_names(first, second)
    denominator = len(set(s_names_first) | set(s_names_second))
    numerator = len(set(s_names_first) & set(s_names_second))

    jaccard = numerator / denominator if denominator > 0 else 0
    print(jaccard)

def print_spearman(first, second):
    s_names_first, s_names_second = get_s_names(first, second)

    print(spearmanr(s_names_first, s_names_second))
    # print(len(set(s_names_first) & set(s_names_second)))

def print_MRR(first, second):
    MRR = 0.0
    s_names_first, s_names_second = get_s_names(first, second)
    for player in s_names_second:
        MRR = MRR + 1/(s_names_first.index(player) + 1)
    MRR = MRR/len(s_names_first)
    print(MRR)

def visualize_density():
    f = open('out_batter.json', 'r', encoding="utf-8")

    jsonData = json.load(f)
    time_array = jsonData['time_array']
    #  "TB", "OBP", "OPS"
    for metric in ["Btype"]:
        print("---")
        print(metric)
        sorted_all_high = get_sorted(metric, 0, time_array, True)
        df = pd.DataFrame(sorted_all_high)
        print(df)

        f, ax = plt.subplots(figsize=(7,6))
        sns.boxplot(x=metric, data=df, whis=[0,100], width=.5, palette="vlag")
        sns.stripplot(x=metric, data=df, size=2, color=".3", linewidth=0)

        ax.xaxis.grid(True)
        ax.set(ylabel="")
        sns.despine(trim=True, left=True)
        plt.show()
    return

def compare_stats(max):
    f = open('out_batter.json', 'r', encoding="utf-8")

    jsonData = json.load(f)
    time_array = jsonData['time_array']

    for metric in ["Btype", "TB", "OBP", "OPS"]:
        print("---")
        print(metric)

        sorted_all_high = get_sorted(metric, 11, time_array, True)
        sorted_all_low = get_sorted(metric, 11, time_array, False)

        sorted_first_high = get_sorted(metric, 0, time_array, True)[0:max]
        sorted_second_high = get_sorted(metric, 11, time_array, True)[0:max]

        print_spearman(sorted_first_high, sorted_second_high)
        print("MRR")
        print_MRR(sorted_all_high, sorted_first_high)
        print("jaccard")
        print_jaccard(sorted_first_high, sorted_second_high)

        sorted_first_low = get_sorted(metric, 0, time_array, False)[0:max]
        sorted_second_low = get_sorted(metric, 11, time_array, False)[0:max]

        print_spearman(sorted_first_low, sorted_second_low)
        print("MRR")
        print_MRR(sorted_all_low, sorted_first_low)
        print("jaccard")
        print_jaccard(sorted_first_low, sorted_second_low)

if __name__ == "__main__":
    visualize_density()
