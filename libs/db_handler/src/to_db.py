import sqlite3
from pathlib import Path
from typing import TypeVar

from modules.persons.src.common.csv_column_names import CLEANED_PERSON_COLUMN_NAMES

T = TypeVar("T")


def save_to_db(input_data: list[T], output_file_path: str) -> None:
    Path(output_file_path).parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(output_file_path)
    cursor = conn.cursor()

    table_name = "persons"
    columns = ", ".join(f"{col} TEXT" for col in CLEANED_PERSON_COLUMN_NAMES)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        )
    """)

    placeholders = ", ".join("?" for _ in CLEANED_PERSON_COLUMN_NAMES)
    insert_query = f"INSERT INTO {table_name} ({', '.join(CLEANED_PERSON_COLUMN_NAMES)}) VALUES ({placeholders})"

    rows = [
        tuple(str(getattr(obj, col, "")) for col in CLEANED_PERSON_COLUMN_NAMES)
        for obj in input_data
    ]

    cursor.executemany(insert_query, rows)

    conn.commit()
    conn.close()
