import sqlite3
from pathlib import Path

from modules.panel_data.src.constants.paths import PANEL_DATA_OUTPUT_PATH
from modules.panel_data.src.constants.table_definitions.gender_factors_table import (
    GENDER_FACTORS_TABLE_COLUMNS,
    GENDER_FACTORS_TABLE_NAME,
)
from modules.panel_data.src.constants.table_definitions.panel_data_table import (
    PANEL_DATA_TABLE_COLUMNS,
    PANEL_DATA_TABLE_NAME,
)
from modules.panel_data.src.constants.table_definitions.gender_factors_definitions_table import (
    GENDER_FACTORS_DEFINITIONS_TABLE_NAME,
    GENDER_FACTORS_DEFINITIONS_TABLE_COLUMNS,
    GENDER_FACTORS_DEFINITIONS,
)
from modules.shared.common.logger import setup_logging
from modules.shared.constants.paths import DATA_PATH


def setup_database_tables(file_path: Path) -> None:
    file_path.touch(exist_ok=True)
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()

    cursor.execute(
        f"CREATE TABLE {GENDER_FACTORS_TABLE_NAME} ({GENDER_FACTORS_TABLE_COLUMNS})"
    )
    cursor.execute(
        f"CREATE TABLE IF NOT EXISTS {PANEL_DATA_TABLE_NAME} ({PANEL_DATA_TABLE_COLUMNS})"
    )
    cursor.execute("DROP TABLE IF EXISTS gender_factors_definitions")
    cursor.execute(
        f"CREATE TABLE {GENDER_FACTORS_DEFINITIONS_TABLE_NAME} ({GENDER_FACTORS_DEFINITIONS_TABLE_COLUMNS})"
    )
    cursor.executemany(
        f"INSERT INTO {GENDER_FACTORS_DEFINITIONS_TABLE_NAME} (id, factor_name, weight) VALUES (?, ?, ?)",
        GENDER_FACTORS_DEFINITIONS,
    )

    conn.commit()
    conn.close()


def setup(time_stamp: str) -> None:
    module_directories = [
        DATA_PATH,
        PANEL_DATA_OUTPUT_PATH,
        PANEL_DATA_OUTPUT_PATH / "db",
    ]

    [directory.mkdir(parents=True, exist_ok=True) for directory in module_directories]

    setup_logging(time_stamp, PANEL_DATA_OUTPUT_PATH / "logs")

    setup_database_tables(PANEL_DATA_OUTPUT_PATH / "db" / f"{time_stamp}.db")
