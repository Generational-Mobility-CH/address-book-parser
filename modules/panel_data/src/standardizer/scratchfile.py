from modules.panel_data.src.gender_calculator.constants.female_names_not_ending_in_a import (
    FEMALE_NAMES_NOT_ENDING_IN_A,
)

re_sorted_male_names = sorted(FEMALE_NAMES_NOT_ENDING_IN_A)
for name in re_sorted_male_names:
    print(f'"{name.lower()}",')
