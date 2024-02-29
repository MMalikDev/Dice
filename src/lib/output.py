from typing import List

from lib.utilities import logger


def log_odds(odds: int, combos: int, tampered: int, random: int) -> None:
    plays = tampered + random
    totals = odds // plays

    chances = [
        {
            "conditions": "Regression is applied",
            "value": (totals / odds) * (plays / totals),
        },
        {
            "conditions": "SUM is guessed properly",
            "value": (combos / odds) * (plays / combos),
        },
        {
            "conditions": "BIAS RANGE is guessed properly",
            "value": (random / odds) + (tampered / totals),
        },
        {
            "conditions": "BIAS SUM value is guessed properly",
            "value": (random / odds) + (tampered / combos),
        },
    ]

    for chance in chances:
        msg = f"{chance['conditions']}: {chance['value']*100:.6f}% "
        logger.info(msg)


def log_chances(plays: int, odds: int) -> None:
    msg = f"{(plays/odds)*100:.12f}%" + "\n\n"
    msg += f"{plays} in {odds:,}" + "\n\n"
    msg += f"1 in {(odds//plays):,}"

    logger.info(msg.replace(",", " "))


def log_play(play: List[int]) -> None:
    nums = " ".join([f"{i:02d}" for i in play])

    logger.info(f"{nums} ({sum(play)})")
