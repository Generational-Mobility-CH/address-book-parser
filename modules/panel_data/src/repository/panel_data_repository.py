import sqlite3
from pathlib import Path

from modules.panel_data.src.repository.constants.panel_data_table import (
    PANEL_DATA_TABLE_NAME,
    PANEL_DATA_TABLE_COLUMNS_NAMES,
    PANEL_DATA_TABLE_COLUMNS,
)
from modules.panel_data.src.models.new_person import NewPerson
from modules.shared.repository.repository import Repository


class PanelDataRepository(Repository):
    table_name = PANEL_DATA_TABLE_NAME

    def __init__(self, column_names=PANEL_DATA_TABLE_COLUMNS_NAMES) -> None:
        self.cols_str = ", ".join(column_names)
        self.placeholders = ", ".join(["?"] * len(column_names))

    def save(self, persons_collection: list[NewPerson], output_path: Path) -> None:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        with sqlite3.connect(output_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"CREATE TABLE IF NOT EXISTS {PANEL_DATA_TABLE_NAME} ({PANEL_DATA_TABLE_COLUMNS})"
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
                    str(getattr(person, "street_name", "")),
                    str(getattr(person, "house_number", "")),
                    str(getattr(person, "job", "")),
                    str(getattr(person, "year", "")),
                    str(getattr(person, "pdf_page_number", "")),
                    str(getattr(person, "original_names", "")),
                )
                for person in persons_collection
            ]

            cursor.executemany(
                f"INSERT INTO {PANEL_DATA_TABLE_NAME} ({self.cols_str}) VALUES ({self.placeholders})",
                rows,
            )
