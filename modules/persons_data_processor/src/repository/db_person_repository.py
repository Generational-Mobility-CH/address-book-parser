import sqlite3
from pathlib import Path

from .constants.db_column_names import DB_COLUMN_NAMES
from modules.shared.repository.repository import Repository
from ..constants.database_table_names import PERSONS_ENTRIES_TABLE_NAME
from ..models.person.person import Person

# TODO: make column definition variable (e.g. pass as argument) instead of using const file
FIELDS_DECLARATION = ", ".join(f"{field_name} TEXT" for field_name in DB_COLUMN_NAMES)
PLACEHOLDERS = ", ".join(["?"] * len(DB_COLUMN_NAMES))
COLUMNS_STR = ", ".join(DB_COLUMN_NAMES)


class DbPersonRepository(Repository):
    def __init__(self, table_name: str = PERSONS_ENTRIES_TABLE_NAME) -> None:
        self.table_name = table_name

    def save(self, persons_collection: list[Person], output_path: Path) -> None:
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        conn = sqlite3.connect(output_path)
        cursor = conn.cursor()
        cursor.execute(
            f"CREATE TABLE IF NOT EXISTS {self.table_name} ({FIELDS_DECLARATION})"
        )
        cursor.execute("PRAGMA synchronous = OFF")
        cursor.execute("PRAGMA journal_mode = MEMORY")

        rows = [
            (
                str(getattr(person, "original_names", "")),
                person.address.street_name,
                person.address.house_number,
                str(getattr(person, "job", "")),
                str(getattr(person, "year", "")),
                str(getattr(person, "pdf_page_number", "")),
            )
            for person in persons_collection
        ]

        cursor.executemany(
            f"INSERT INTO {self.table_name} ({COLUMNS_STR}) VALUES ({PLACEHOLDERS})",
            rows,
        )

        conn.commit()
        conn.close()
