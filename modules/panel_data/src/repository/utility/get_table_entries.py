import sqlite3
from pathlib import Path
from typing import TypeVar, Optional

T = TypeVar("T")


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
