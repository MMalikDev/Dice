import itertools
import re
from collections import Counter
from typing import Any, Dict, List

import pandas as pd

from lib.utilities import logger


# ---------------------------------------------------------------------- #
# Helper Functions
# ---------------------------------------------------------------------- #
def save_file(data: Dict[str, List[int]], filepath: str) -> None:
    df = pd.DataFrame(data)
    df.to_csv(filepath, index=False)

    logger.info(f"DataFrame saved @ {filepath}")


def format_draw(draw: str) -> List[int]:
    nums = re.split(" ", str(draw).strip())
    return [int(i) for i in nums]


def format_extra(draw: str) -> List[int]:
    nums = re.split("\r|\n", str(draw).strip())
    return [format_draw(i) for i in nums] if "nan" not in nums else 0


# ---------------------------------------------------------------------- #
# Data Functions
# ---------------------------------------------------------------------- #
def get_combinations(n: int, length: int) -> Dict[str, Any]:
    numbers = [i for i in range(1, n + 1)]
    combinations = itertools.combinations(numbers, length)
    sums = map(sum, combinations)

    return {"Combination": combinations, "Sum": sums}


def get_frequencies(n: int, length: int) -> Dict[str, Any]:
    numbers = [i for i in range(1, n + 1)]
    combinations = itertools.combinations(numbers, length)
    sums = map(sum, combinations)
    count = Counter(sums)

    return {"Sum": count.keys(), "Frequency": count.values()}


def get_past_result(data: pd.Series, file: str) -> None:
    data = data.dropna().astype(int).to_list()
    count = Counter(sorted(data))
    sums = {"Sum": count.keys(), "Frequency": count.values()}

    save_file(sums, file)


def get_file_results(source: str, file: str) -> None:
    df = pd.read_csv(source)
    data = df.Sum

    get_past_result(data, file)


def get_extra(data: pd.Series, file: str) -> None:
    extras = []
    subset = data.map(format_extra)
    df = pd.DataFrame(columns=["Extra", "Sum"])

    for sub in subset[subset != 0]:
        extras += sub
    for extra in extras:
        new_row = pd.DataFrame([[extra, sum(extra)]], columns=df.columns)
        df = pd.concat([df, new_row], ignore_index=True)

    save_file(df, file)


def get_bonus(df: pd.DataFrame, file: str) -> None:
    draws = df.Draw.map(format_draw).to_list()
    bonus = df.Bonus.to_list()

    df = pd.DataFrame(columns=["Bonus", "Sum"])
    for draw, num in zip(draws, bonus):
        if not draw:
            continue

        for i in range(len(draw)):
            roll = draw.copy()
            roll[i] = num
            new_row = pd.DataFrame([[roll, int(sum(roll))]], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)

    save_file(df, file)


# ---------------------------------------------------------------------- #
# Core Functions
# ---------------------------------------------------------------------- #
def get_all_results(n: int, length: int, file: str) -> None:
    frequencies = get_frequencies(n, length)

    save_file(frequencies, file)


def describe_data(filepath: str) -> None:
    df = pd.read_csv(filepath)
    logger.info(df.describe())
    df.info()
