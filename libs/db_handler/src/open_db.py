import sqlite3
import pandas as pd
from pathlib import Path

from modules.persons_data_processor.src.repository.supported_file_types import (
    SupportedFileTypes,
)


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


def load_table(db_path: Path, table: str) -> pd.DataFrame:
    if not db_path.exists():
        raise FileNotFoundError(f"File {db_path} does not exist")

    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    conn.close()

    return df
