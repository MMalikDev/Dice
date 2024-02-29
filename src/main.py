from typing import List

from lib import analysis, dice, output
from lib.utilities import load_variable, logger


# ---------------------------------------------------------------------- #
# Helper Functions
# ---------------------------------------------------------------------- #
def log_results(
    odds: int, combo: int, tampered: int, random: int, plays: List[List[int]]
) -> int:
    DELIMITER = f"\n{'-'*50}\n"

    rolls = tampered + random
    logger.info(DELIMITER)

    output.log_odds(odds, combo, tampered, random)
    logger.info(DELIMITER)
    output.log_chances(rolls, odds)
    logger.info(DELIMITER)

    for play in plays:
        output.log_play(play)

    logger.info(DELIMITER)


def get_odds(dies: int, sides: int) -> int:
    a, b = 1, 1
    for i in range(sides - dies + 1, sides + 1):
        a *= i
    for i in range(1, dies + 1):
        b *= i

    return a // b


# ---------------------------------------------------------------------- #
# Main Functions                                                         #
# ---------------------------------------------------------------------- #
def main(dies: int, sides: int, random: int, tampered: int, X: bool) -> None:
    FILEPATH, NUMS = "./data/", 20

    mode, bias, mean, dev = analysis.get_stats(dies, sides, NUMS, FILEPATH, X)
    odds = get_odds(dies, sides)
    plays = []

    for i in range(tampered):
        roll = dice.roll_bias(dies, sides, bias, bool(i % 2), mean, dev)
        plays.append(roll)
    for _ in range(random):
        roll = dice.roll_shuffle(dies, sides)
        plays.append(roll)

    logger.info(sorted(bias))
    log_results(odds, mode, tampered, random, plays)


if __name__ == "__main__":
    tampered, random = load_variable("TAMPERED", "2"), load_variable("RANDOM", "1")
    dies, sides = load_variable("DIES", "7"), load_variable("SIDES", "50")
    X = load_variable("X", "0") in ["TRUE", "True", "1"]

    main(int(dies), int(sides), int(random), int(tampered), bool(X))
