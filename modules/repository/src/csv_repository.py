import csv
from logging import getLogger
from pathlib import Path
from typing import Optional, TypeVar

from modules.repository.src.repository import Repository

T = TypeVar("T")

logger = getLogger(__name__)


class CsvRepository(Repository):
    def __init__(self, column_names: Optional[list[str]] = None) -> None:
        """
        Arguments:
            column_names: If you only want a subset of the object's attributes in the csv, you may provide a list containing only the relevant column names.
            This in mainly used for testing purposes in this project.
        """
        self.column_names = column_names

    def save(self, collection: list[T], output_path: Path) -> None:
        if not collection:
            raise ValueError("Provided collection must not be empty.")

        objects_as_dicts = [obj.__dict__ for obj in collection]

        if self.column_names:
            objects_as_dicts = [
                {key: val for key, val in obj.items() if key in self.column_names}
                for obj in objects_as_dicts
            ]

        objects_as_dicts_titled = [
            {
                key: (val.title() if isinstance(val, str) else val)
                for key, val in obj.items()
            }
            for obj in objects_as_dicts
        ]

        with output_path.open(mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=self.column_names
                if self.column_names
                else objects_as_dicts[0].keys(),
            )
            writer.writeheader()
            writer.writerows(objects_as_dicts_titled)

        logger.info(f"Saved data to {output_path}")

    def get_table_entries(
        self, db_path: Path, table_name: str, entries_filter: Optional[str] = None
    ) -> list[T]:
        # TODO: implement get_table_entries() for csv files
        pass
