import csv
import os
from typing import TypeVar


T = TypeVar("T")

def save_to_csv(input_data: list[T], output_file_path: str) -> None:
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    with open(output_file_path, "w", newline="", encoding="utf-8") as csv_file:
        column_names = ["names", "job", "address", "year", "pdf_page_number", "person_id"]
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        writer.writeheader()

        for obj in input_data:
            writer.writerow({name: getattr(obj, name) for name in column_names})
