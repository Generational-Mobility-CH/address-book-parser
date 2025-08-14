import sqlite3
from pathlib import Path
from typing import TypeVar

from libs.db_handler.src.constants.db_column_names import DB_COLUMN_NAMES
from modules.persons_data_processor.src.models.person.person import Person

T = TypeVar("T")

# TODO: make column definition variable (e.g. pass as argument) instead of using const file
FIELDS_DECLARATION = ", ".join(f"{field_name} TEXT" for field_name in DB_COLUMN_NAMES)
PLACEHOLDERS = ", ".join(["?"] * len(DB_COLUMN_NAMES))
COLUMNS_STR = ", ".join(DB_COLUMN_NAMES)


def save_to_db(
    input_data: list[Person], output_file_path: Path, table_name: str
) -> None:
    Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(output_file_path)
    cursor = conn.cursor()
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({FIELDS_DECLARATION})")
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
        for person in input_data
    ]

    cursor.executemany(
        f"INSERT INTO {table_name} ({COLUMNS_STR}) VALUES ({PLACEHOLDERS})",
        rows,
    )

    conn.commit()
    conn.close()
