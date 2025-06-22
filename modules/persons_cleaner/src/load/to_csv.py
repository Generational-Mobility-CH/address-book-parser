import csv
from typing import TypeVar

from modules.common.csv_column_names import CLEANED_PERSON_COLUMN_NAMES

T = TypeVar("T")


def save_to_csv(input_data: list[T], output_file_path: str) -> None:
    with open(output_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CLEANED_PERSON_COLUMN_NAMES)
        writer.writeheader()

        for obj in input_data:
            writer.writerow({name: getattr(obj, name) for name in CLEANED_PERSON_COLUMN_NAMES})
