import csv
from logging import getLogger
from pathlib import Path
from typing import List, Optional, TypeVar

from .person_repository import PersonRepository
from ..models.person.person import Person

T = TypeVar("T")

logger = getLogger(__name__)


class CsvPersonRepository(PersonRepository):
    def __init__(self, column_names: Optional[List[str]] = None) -> None:
        self.column_names = column_names

    def save(self, persons_collection: List[Person], output_path: Path) -> None:
        if not persons_collection:
            raise ValueError("Persons collection must not be empty.")

        column_names = self.column_names or _get_column_names_from_object(
            persons_collection[0]
        )

        with output_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=column_names)
            writer.writeheader()

            for person in persons_collection:
                flattened_person = _flatten_object(person)
                row = {}
                for col_name in column_names:
                    if col_name not in flattened_person:
                        logger.error(f"Column {col_name} not found in object {person}")

                    row[col_name] = flattened_person[col_name]

                writer.writerow(row)


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
