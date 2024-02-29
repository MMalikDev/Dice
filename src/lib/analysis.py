import os
from typing import Dict, List, Tuple

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd

from lib import data


# ---------------------------------------------------------------------- #
# Helper Functions
# ---------------------------------------------------------------------- #
def show_distribution(base: dict, reference: dict, title: str) -> None:
    matplotlib.use("QtAgg")
    plt.style.use("dark_background")
    plt.figure(f"Distribution: {title}", facecolor="black", figsize=(18, 8))

    plt.bar(base.keys(), base.values(), color="#9FBFFF", alpha=0.8)
    plt.bar(reference.keys(), reference.values(), color="#ED3040", alpha=0.8)

    plt.gca().get_yaxis().set_visible(False)
    plt.tight_layout()

    plt.savefig(f"./views/{title}.svg", format="svg")
    plt.show()


def get_percent_totals(df: pd.DataFrame) -> Dict[int, float]:
    df = df.set_index("Sum")
    total = df.Frequency.sum()
    df["Chances"] = df.Frequency / total

    return df.to_dict()["Chances"]


def show_graph(base: pd.DataFrame, reference: pd.DataFrame, title: str) -> None:
    base = get_percent_totals(base)
    reference = get_percent_totals(reference)
    show_distribution(base, reference, title)


# ---------------------------------------------------------------------- #
# Core Functions
# ---------------------------------------------------------------------- #
def get_bias(nums: int, possible: pd.DataFrame, past: pd.DataFrame) -> List[int]:
    possible = get_percent_totals(possible)
    past = get_percent_totals(past)
    variances = dict()

    for k, v in possible.items():
        variances[k] = v - past.get(k, 0)

    bias = sorted(variances.items(), key=lambda item: item[1])
    bias = [i for i, _ in bias[-nums:]]
    return bias


def get_deviation(df: pd.DataFrame) -> Tuple[int, float]:
    mean = int(df.mean().Sum)
    std_dev = df.std().Sum
    return mean, std_dev


def get_mode(df: pd.DataFrame) -> int:
    frequencies = df.Frequency.to_dict()
    return frequencies[int(df.Sum.mean())]


# ---------------------------------------------------------------------- #
# Main Function
# ---------------------------------------------------------------------- #
def get_stats(dies: int, sides: int, nums: int, path: str, X: bool) -> Tuple[int, int]:
    past = path + "past.csv"
    draws = path + "draws.csv"
    possible = path + "possible.csv"
    past_data = "Total"

    extra_data = "Extra"
    extra = path + "extra.csv"
    past_extra = path + "past_extra.csv"

    bonus = path + "bonus.csv"
    bonus_data = ["Draw", "Bonus"]
    past_bonus = path + "past_bonus.csv"

    # Get mandatory data
    if not os.path.exists(draws):
        raise Exception(f"Missing past result data {draws}")

    df = pd.read_csv(draws)
    past_data = df[past_data]
    extra_data = df[extra_data]
    bonus_data = df[bonus_data]

    # Configs for past result data
    required = [
        {"file": past, "inputs": (past_data,), "create": data.get_past_result},
        {"file": possible, "inputs": (sides, dies), "create": data.get_all_results},
    ]

    optional = [
        {"file": extra, "inputs": (extra_data,), "create": data.get_extra},
        {"file": bonus, "inputs": (bonus_data,), "create": data.get_bonus},
        {"file": past_extra, "inputs": (extra,), "create": data.get_file_results},
        {"file": past_bonus, "inputs": (bonus,), "create": data.get_file_results},
    ]

    stats = required
    stats += optional

    # Set past result data
    for stat in stats:
        if not os.path.exists(stat["file"]):
            initializer = stat["create"]
            inputs = stat["inputs"] + (stat["file"],)
            initializer(*inputs)

    # Get past result data
    df_past = pd.read_csv(past)
    df_possible = pd.read_csv(possible)
    show_graph(df_possible, df_past, "Winners")

    # Get Statistic
    mode = get_mode(df_possible)
    bias = get_bias(nums, df_possible, df_past)
    mean, standard_deviation = get_deviation(df_possible)

    if X:
        df_extra = pd.read_csv(past_extra)
        df_bonus = pd.read_csv(past_bonus)
        show_graph(df_possible, df_extra, "Extra")
        show_graph(df_possible, df_bonus, "Bonus")

    return mode, bias, mean, standard_deviation
