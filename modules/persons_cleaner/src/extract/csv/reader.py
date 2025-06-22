import csv
import os


def read_csv(file_path: str) -> list[str]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    result = []
    with open(file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            row_string = ",".join(row)
            result.append(row_string)

    return result
