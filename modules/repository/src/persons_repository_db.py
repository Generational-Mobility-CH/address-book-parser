import sqlite3
from logging import getLogger
from pathlib import Path
from typing import Optional

from modules.repository.src.constants.table_definitions import (
    PERSONS_TABLE_NAME,
    PERSONS_TABLE_COLUMNS_NAMES,
    PERSONS_TABLE_COLUMNS,
)
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.repository.src.repository import Repository, T

_logger = getLogger(__name__)


class PersonsRepositoryDb(Repository):
    table_name = PERSONS_TABLE_NAME

    def __init__(self, column_names=PERSONS_TABLE_COLUMNS_NAMES) -> None:
        self.cols_str = ", ".join(column_names)
        self.placeholders = ", ".join(["?"] * len(column_names))

    def save(self, persons_collection: list[PanelDataEntry], output_path: Path) -> None:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(output_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {PERSONS_TABLE_NAME} ({PERSONS_TABLE_COLUMNS})"
            )
            cursor.execute("PRAGMA synchronous = OFF")
            cursor.execute("PRAGMA journal_mode = MEMORY")

            rows = [
                (
                    str(getattr(person, "first_names", "")),
                    str(getattr(person, "last_names", "")),
                    str(getattr(person, "partner_last_names", "")),
                    str(getattr(person, "gender", "")),
                    str(getattr(person, "gender_confidence", "")),
                    person.address.street_name,
                    person.address.house_number,
                    str(getattr(person, "job", "")),
                    str(getattr(person, "year", "")),
                    str(getattr(person, "pdf_page_number", "")),
                    str(getattr(person, "original_entry", "")),
                )
                for person in persons_collection
            ]

            normalized_rows = [
                tuple(
                    " ".join(attribute.strip().split()).title() for attribute in person
                )
                for person in rows
            ]

            cursor.executemany(
                f"INSERT INTO {PERSONS_TABLE_NAME} ({self.cols_str}) VALUES ({self.placeholders})",
                normalized_rows,
            )

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
                (table_name,),
            )
            if not cursor.fetchone():
                raise ValueError(
                    f"Table '{table_name}' does not exist in the '{db_path}'."
                )

            query = f"SELECT * FROM {table_name}" + (
                entries_filter if entries_filter else ""
            )
            cursor.execute(query)
            rows = cursor.fetchall()

        for row in rows:
            entry_data = dict(zip(PERSONS_TABLE_COLUMNS_NAMES, row))
            entry = PanelDataEntry(**entry_data)
            result.append(entry)

        return result
