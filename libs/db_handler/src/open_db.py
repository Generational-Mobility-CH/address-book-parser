import sqlite3
from pathlib import Path
from typing import TypeVar, Optional

from modules.persons_data_processor.src.repository.supported_file_types import (
    SupportedFileTypes,
)

T = TypeVar("T")


def get_latest_db_file(
    db_path: Path, input_type: SupportedFileTypes = SupportedFileTypes.DB
) -> Path:
    db_files = sorted(
        db_path.glob(f"*.{input_type.value}"),
        key=lambda f: f.stat().st_mtime,
        reverse=True,
    )
    if not db_files:
        raise FileNotFoundError(f"No .{input_type} files found in {db_path}")
    return db_files[0]


def get_table_entries(
    db_path: Path, table_name: str, entries_filter: Optional[str] = None
) -> list[T]:
    if not db_path.exists():
        raise FileNotFoundError(f"File not found: {db_path}")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
    )
    if not cursor.fetchone():
        raise ValueError(f"Table '{table_name}' does not exist in the '{db_path}'.")

    query = f"SELECT * FROM {table_name}" + (entries_filter if entries_filter else "")
    cursor.execute(query)
    rows = cursor.fetchall()

    cursor.close()
    conn.close()

    return rows
