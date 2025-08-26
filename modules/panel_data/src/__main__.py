import sqlite3
from datetime import datetime
from logging import getLogger
from pathlib import Path

import pandas as pd

from libs.db_handler.src.open_db import load_table, get_latest_db_file
from modules.panel_data.src.constants.paths import (
    PANEL_DATA_OUTPUT_PATH,
    PANEL_DATA_INPUT_PATH,
)
from modules.panel_data.src.constants.table_definitions.panel_data_table import (
    PANEL_DATA_TABLE_NAME,
)
from modules.panel_data.src.setup import setup
from modules.panel_data.src.year_linker.data_wrangler import wrangle_dataset
from modules.persons_data_processor.src.constants.database_table_names import (
    PERSONS_ENTRIES_TABLE_NAME,
)

logger = getLogger(__name__)


def main(input_path: Path, output_path: Path) -> None:
    logger.info(f"Reading data from {input_path}")
    df = load_table(input_path, PERSONS_ENTRIES_TABLE_NAME)
    df = wrangle_dataset(df, output_path)

    with pd.option_context("display.max_columns", None):
        logger.info("\n%s", df.head())

    df.to_sql(
        PANEL_DATA_TABLE_NAME,
        sqlite3.connect(output_path),
        if_exists="replace",
        index=False,
    )

    # link_two_years("1920", "1921", df)


if __name__ == "__main__":
    demo_input_path = get_latest_db_file(PANEL_DATA_INPUT_PATH)
    time_stamp = f"{datetime.now():%b %d - %H%M}"
    demo_output_path = PANEL_DATA_OUTPUT_PATH / "db" / f"{time_stamp}.db"

    setup(time_stamp)
    main(demo_input_path, demo_output_path)
