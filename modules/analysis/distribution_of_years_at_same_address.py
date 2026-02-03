from collections import Counter

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import FuncFormatter

from modules.repository.src.constants.table_definitions import (
    PERSONS_TABLE_NAME,
)
from modules.repository.src.persons_repository_db import PersonsRepositoryDb
from modules.shared.common.paths import DATA_PATH
from modules.shared.models.panel_data_entry import PanelDataEntry


def _count_years_at_same_address(data: list[PanelDataEntry]) -> dict[str, int]:
    """
    Count how many years each person lived at a concrete address.
    The key to link the person across the years is: last_names + first_names + address
    """
    result = dict()

    for entry in data:
        key = f"{entry.last_names}-{entry.first_names}-{entry.address}"
        if key not in result:
            result[key] = 1
        else:
            result[key] += 1

    return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))


if __name__ == "__main__":
    newest_db_file = "2026.01.29-panel_dataset.db"

    entries = PersonsRepositoryDb().get_table_entries(
        DATA_PATH / "db" / newest_db_file, PERSONS_TABLE_NAME
    )

    persons_and_years_at_same_address = _count_years_at_same_address(entries)

    duration_distribution = dict(Counter(persons_and_years_at_same_address.values()))

    # Display results for years 1-3 separately, in order not to distort the plot
    for years in [1, 2, 3]:
        print(f"{years} years: {duration_distribution[years]} persons")
        duration_distribution.pop(years)

    # Ignore results where < 100 people where found
    years_duration = [
        years for years, count in duration_distribution.items() if count >= 100
    ]
    number_of_people = [
        count for years, count in duration_distribution.items() if count >= 100
    ]

    # Create the plot
    plt.figure(figsize=(10, 5))
    plt.title("How many persons lived x years at the same address?")
    plt.bar(years_duration, number_of_people, color="skyblue", width=0.5)

    plt.xlabel("Years at the same address")
    x_step_size = 2
    x_max_value = 50 + x_step_size
    plt.xticks(np.arange(0, x_max_value, x_step_size))

    plt.ylabel("Number of persons")
    y_step_size = 5000
    y_max_value = 100000 + y_step_size
    plt.yticks(np.arange(0, y_max_value, y_step_size))
    plt.gca().yaxis.set_major_formatter(
        FuncFormatter(lambda value, _: f"{int(value):,}")
    )  # Add commas to numbers, e.g. 1000 -> 1'000
    plt.grid(axis="y")

    plt.show()
