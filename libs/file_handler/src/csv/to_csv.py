import csv
from logging import getLogger
from pathlib import Path
from typing import TypeVar, Optional

T = TypeVar("T")

logger = getLogger(__name__)


def _get_column_names_from_object(obj: T) -> list[str]:
    result = []
    obj_keys = _flatten_object(obj).keys()

    for key in obj_keys:
        if (
            not key.startswith("__")
            and not key.startswith("_")
            and len(key.split("_")) in (1, 2, 4)
        ):
            result.append(key)

    return result


def _flatten_object(obj: T, parent_key="", sep="_") -> dict:
    items = {}

    for key in dir(obj):
        if not key.startswith("__"):
            value = getattr(obj, key)
            new_key = (
                f"{parent_key}{key}" if parent_key == "" else f"{parent_key}{sep}{key}"
            )
            if isinstance(value, object) and not isinstance(
                value, (str, int, float, bool)
            ):
                items.update(_flatten_object(value, new_key, sep=sep))
            else:
                items[new_key] = value

    return items


def save_to_csv(
    input_data: list[T],
    output_file_path: Path,
    column_names: Optional[list[str]] = None,
) -> None:
    if not input_data:
        raise ValueError("Input data must not be empty.")

    column_names = column_names or _get_column_names_from_object(input_data[0])

    with output_file_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=column_names)
        writer.writeheader()

        for obj in input_data:
            flattened_obj = _flatten_object(obj)
            row = {}
            for col_name in column_names:
                if col_name not in flattened_obj:
                    logger.error(f"Column {col_name} not found in object {obj}")

                row[col_name] = flattened_obj[col_name]

            writer.writerow(row)
