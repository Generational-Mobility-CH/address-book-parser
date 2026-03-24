import sqlite3
from logging import getLogger
from pathlib import Path
from typing import Optional

import pandas as pd

from src.repository.src.constants.table_definitions import (
    PERSONS_TABLE_NAME,
    PERSONS_TABLE_COLUMNS_NAMES,
)
from src.repository.src.repository import Repository, T, prepare_data
from src.shared.models.panel_data_entry import PanelDataEntry

_logger = getLogger(__name__)


class DbRepository(Repository):
    def __init__(self, table_name=PERSONS_TABLE_NAME) -> None:
        self.table_name = table_name

    def save(self, data: list[PanelDataEntry], output_path: Path) -> None:
        if not data:
            _logger.warning(
                "No data provided. Exiting without writing to the database."
            )
            return

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(output_path) as conn:
            df = pd.DataFrame(prepare_data(data))
            df.to_sql(self.table_name, conn, if_exists="append", index=False)

        _logger.info(f"Saved persons to '{output_path}'")

    def get_table_entries(
        self, db_path: Path, table_name: str, entries_filter: Optional[str] = None
    ) -> list[T]:
        result = []

        if not db_path.exists():
            raise FileNotFoundError(f"File not found: {db_path}")

        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                (self.table_name,),
            )
            if not cursor.fetchone():
                raise ValueError(
                    f"Table '{self.table_name}' does not exist in the '{db_path}'."
                )

            query = f"SELECT * FROM {self.table_name}" + (
                entries_filter if entries_filter else ""
            )
            cursor.execute(query)
            rows = cursor.fetchall()
        # TODO: refactor with new __dict__ attribute in base class
        for row in rows:
            entry_data = dict(zip(PERSONS_TABLE_COLUMNS_NAMES, row))
            entry = PanelDataEntry(**entry_data)
            result.append(entry)

        return result
