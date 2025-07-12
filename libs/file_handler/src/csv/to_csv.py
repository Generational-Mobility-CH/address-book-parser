import csv
from pathlib import Path
from typing import TypeVar, Optional

T = TypeVar("T")


def save_to_csv(
    input_data: list[T],
    output_file_path: Path,
    column_names: Optional[list[str]] = None,
) -> None:
    if not input_data:
        raise ValueError("Input data must not be empty.")

    if column_names:
        fieldnames = column_names
    else:
        first = input_data[0]
        if isinstance(first, dict):
            fieldnames = list(first.keys())
        else:
            fieldnames = [
                attr
                for attr in dir(first)
                if not attr.startswith("_") and not callable(getattr(first, attr))
            ]

    with output_file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for obj in input_data:
            if isinstance(obj, dict):
                row = obj
            else:
                row = {name: getattr(obj, name, None) for name in fieldnames}

            writer.writerow(row)
