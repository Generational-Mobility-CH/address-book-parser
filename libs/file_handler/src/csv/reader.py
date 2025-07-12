import csv
from pathlib import Path


def read_csv(file_path: Path) -> list[str]:
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    result = []
    with file_path.open(mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            row_string = ",".join(row)
            result.append(row_string)

    return result
