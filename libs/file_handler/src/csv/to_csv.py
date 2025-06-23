import csv
from typing import TypeVar


T = TypeVar("T")


def save_to_csv(input_data: list[T], output_file_path: str, column_names: list[str] = None) -> None:
    if not input_data:
        raise ValueError("input_data must not be empty.")

    if column_names:
        fieldnames = column_names
    elif input_data:
        first = input_data[0]
        if isinstance(first, dict):
            fieldnames = list(first.keys())
        else:
            fieldnames = [attr for attr in dir(first) if not attr.startswith("_") and not callable(getattr(first, attr))]
    else:
        fieldnames = input_data[0]

    with open(output_file_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for obj in input_data:
            row = (
                obj if isinstance(obj, dict)
                else {name: getattr(obj, name, None) for name in fieldnames}
            )
            writer.writerow(row)
