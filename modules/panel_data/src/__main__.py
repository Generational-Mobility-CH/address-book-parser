import sqlite3
import time
import pandas as pd

from datetime import datetime
from logging import getLogger
from pathlib import Path
from time import strftime

from libs.db_handler.src.open_db import load_table, get_latest_db_file
from modules.persons_data_processor.src.common.logger import setup_logging
from modules.persons_data_processor.src.constants import (
    PERSONS_ENTRIES_TABLE,
)
from modules.panel_data.src.common.paths import (
    PANEL_DATA_OUTPUT_PATH,
    PANEL_DATA_INPUT_PATH,
)
from modules.panel_data.src.constants.table_names import PANEL_DATA_PERSON_TABLE
from modules.panel_data.src.year_linker.data_wrangler import wrangle_dataset

logger = getLogger(__name__)


def main(input_path: Path, output_path: Path) -> None:
    df = load_table(input_path, PERSONS_ENTRIES_TABLE)
    df = wrangle_dataset(df)
    logger.info(f"Reading data from {input_path}")
    with pd.option_context("display.max_columns", None):
        logger.info("\n%s", df.head())

    df.to_sql(
        PANEL_DATA_PERSON_TABLE,
        sqlite3.connect(output_path),
        if_exists="replace",
        index=False,
    )

    # link_two_years("1920", "1921", df)


if __name__ == "__main__":
    PANEL_DATA_OUTPUT_PATH.mkdir(exist_ok=True)
    (PANEL_DATA_OUTPUT_PATH / "db").mkdir(exist_ok=True)
    (PANEL_DATA_OUTPUT_PATH / "logs").mkdir(exist_ok=True)

    demo_input_path = get_latest_db_file(PANEL_DATA_INPUT_PATH)
    time_stamp = f"{datetime.now():%b %d - %H%M}"
    demo_output_path = Path(PANEL_DATA_OUTPUT_PATH) / "db" / f"{time_stamp}.db"

    setup_logging(time_stamp, PANEL_DATA_OUTPUT_PATH / "logs")
    start_time = time.time()

    main(demo_input_path, demo_output_path)

    logger.info(
        strftime("Execution time: %M min %S s", time.gmtime(time.time() - start_time))
    )
