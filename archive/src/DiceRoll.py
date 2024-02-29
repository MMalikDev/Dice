import random
from functools import reduce

from DiceRoll_Bias import roll_dice_with_bias


def roll_dice_loop(dice_Qty, side_Qty):
    results = []
    min = 1
    max = side_Qty
    for die in range(dice_Qty):
        roll = random.randint(min, max)
        while roll in results:
            roll = random.randint(min, max)
        results.append(roll)
    results.sort()
    return results


def roll_dice_fast(dice_Qty, side_Qty):
    results = [0] * dice_Qty
    available_nums = [x for x in range(side_Qty + 1) if x > 0]
    for die in range(dice_Qty):
        roll = random.choice(available_nums)
        available_nums.remove(roll)
        results[die] = roll
    results.sort()
    return results


def roll_dice(dice_Qty, side_Qty):
    results = []
    available_nums = [x for x in range(1, side_Qty + 1)]
    for _ in range(dice_Qty):
        roll = random.choice(available_nums)
        available_nums.remove(roll)
        results.append(roll)
    results.sort()
    return results


if __name__ == "__main__":
    plays = 3
    dices = 7
    sides = 50

    roll_dice_with_bias(dices, sides, True)
    roll_dice_with_bias(dices, sides, False)

    print("\n", *roll_dice(dices, sides), "\n\n\n\n")

    # """

    top = reduce(lambda x, y: x * y, [x for x in range(1, dices + 1)])
    bottom = reduce(
        lambda x, y: x * y, [x for x in range(sides + 1) if x > (sides - dices)]
    )
    odds = int((bottom / top))

    chances = f"{(plays/odds)*100:.8f}% of winning".replace(",", " ")
    fraction = f"{plays} chance in {odds:,}".replace(",", " ")
    chances_fraction = f"1 in {int(odds/plays):,}".replace(",", " ")

    print(chances_fraction, "\n")
    print(chances, "\n")

    print(fraction, "\n\n")

    # """

    # """
    random_play = 1
    bias_play = 2
    best_sums_comb = 1089264
    best_sums_range = 33824954

    print(
        f"{((best_sums_range/odds)*(plays/best_sums_range))*100:.6f}% if regression is applied\n"
    )
    print(
        f"{((best_sums_comb/odds)*(plays/best_sums_comb))*100:.6f}% if sum is guessed properly\n"
    )
    print(
        f"{((random_play/odds)+(bias_play/best_sums_range))*100:.6f}% if bias range is guessed properly\n"
    )
    print(
        f"{((random_play/odds)+(bias_play/best_sums_comb))*100:.6f}% if bias sum is guessed properly\n"
    )
    # """
