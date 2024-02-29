import random
from typing import List


def roll_loop(dies: int, sides: int) -> List[int]:
    results = list()

    for _ in range(dies):
        roll = random.randint(1, sides)
        while roll in results:
            roll = random.randint(1, sides)

        results.append(roll)
    return sorted(results)


def roll_remove(dies: int, sides: int) -> List[int]:
    nums = [i + 1 for i in range(sides)]
    results = list()

    for _ in range(dies):
        roll = random.choice(nums)
        nums.remove(roll)

        results.append(roll)
    return sorted(results)


def roll_shuffle(dies: int, sides: int) -> List[int]:
    nums = [i + 1 for i in range(sides)]
    random.shuffle(nums)

    return sorted(nums[:dies])


def roll_bias(
    dies: int,
    sides: int,
    bias: List[int],
    trust: bool,
    mean: float,
    deviation: float,
) -> List[int]:
    mean = int(mean)
    deviation = int(deviation)

    low, high = mean - deviation, mean + deviation
    distribution = [i for i in range(low, high + 1)]
    targets = bias if trust else [i for i in distribution if i not in bias]

    results = roll_shuffle(dies, sides)
    while sum(results) not in targets:
        results = roll_shuffle(dies, sides)
    return sorted(results)
