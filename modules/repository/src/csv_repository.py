from logging import getLogger
from pathlib import Path
from typing import Optional, TypeVar

import pandas as pd

from modules.repository.src.repository import Repository, prepare_data

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

    def save(self, data: list[T], output_path: Path) -> None:
        if not data:
            raise ValueError("Provided collection must not be empty.")

        df = pd.DataFrame(prepare_data(data))
        df.to_csv(output_path, index=False, columns=self.column_names, encoding="utf-8")

        logger.info(f"Saved data to {output_path}")

    def get_table_entries(
        self, db_path: Path, table_name: str, entries_filter: Optional[str] = None
    ) -> list[T]:
        # TODO: implement get_table_entries() for csv files
        pass
