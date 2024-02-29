from collections import Counter
from itertools import combinations

import pandas as pd


def create_Outcomes(max_digit, numbers_per_combination):
    # Get all possible combinations
    available_digits = [x for x in range(max_digit + 1) if x != 0]
    possible_combinations = list(
        combinations(available_digits, numbers_per_combination)
    )
    get_sum_of_combination = list(map(sum, possible_combinations))
    mydict = {"Combination": possible_combinations, "Sum": get_sum_of_combination}
    # Create CSV
    file_name = "All_Outcomes.csv"
    df_combinations = pd.DataFrame(mydict)
    df_combinations.to_csv(f"C:/Users/Malik/Desktop/Dice/WIP/Data/{file_name}")
    print(
        f"\nThe following CSV file was created C:/Users/Malik/Desktop/Dice/WIP/Data/{file_name}\n"
    )


def create_Outcomes_sums(max_digit, numbers_per_combination):
    # Get all possible combinations
    available_digits = [x for x in range(max_digit + 1) if x != 0]
    possible_combinations = list(
        combinations(available_digits, numbers_per_combination)
    )
    get_sum_of_combination = list(map(sum, possible_combinations))
    # Count of each sums
    count = dict(Counter(get_sum_of_combination))
    sum_of_combination = [x for x in count]
    frequency = [count[x] for x in count]
    mydict = {"Sum": sum_of_combination, "Frequency": frequency}
    # Create CSV
    file_name = "Sum_Count_of_All_Outcomes.csv"
    df_sum_distribution = pd.DataFrame(mydict)
    df_sum_distribution.to_csv(f"C:/Users/Malik/Desktop/Dice/WIP/Data/{file_name}")
    print(
        f"\nThe following CSV file was created C:/Users/Malik/Desktop/Dice/WIP/Data/{file_name}\n"
    )


# create_Outcomes(50,7)
# create_Outcomes_sums(50,7)

all_Outcomes_df = pd.read_csv("WIP/Data/All_Outcomes.csv")
all_Outcomes_df = all_Outcomes_df[["Combination", "Sum"]]

info = all_Outcomes_df.info()
describe = all_Outcomes_df.describe()

print("\n", describe, "\n")
