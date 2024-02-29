import random


def roll_dice_with_bias(dice_Qty, side_Qty, Trust):
    results = []

    # Mean =
    # standard deviation (SD) =
    distribution_Low = 140  # - 1 SD from Mean =
    distribution_high = 190  # + 1 SD from Mean =
    distribution_list = [x for x in range(distribution_Low, distribution_high + 1)]

    Gold = []
    Cheat = [
        135,
        138,
        140,
        144,
        155,
        156,
        157,
        158,
        160,
        161,
        162,
        163,
        174,
        175,
        176,
        178,
        184,
        185,
        186,
        187,
    ]

    if Trust:
        Gold += Cheat
    else:
        Gold = [x for x in distribution_list if x not in Cheat]

    while sum(results) not in Gold:
        results.clear()
        available_nums = [x for x in range(1, side_Qty + 1)]
        for _ in range(dice_Qty):
            roll = random.choice(available_nums)
            available_nums.remove(roll)
            results.append(roll)

    results.sort()
    print("\n", *results)
    print("\n", (sum(results)), "\n")
    return results


if __name__ == "__main__":
    roll_dice_with_bias(7, 50, True)
    roll_dice_with_bias(7, 50, False)
