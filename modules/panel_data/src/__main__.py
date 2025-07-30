import sqlite3
import time
import pandas as pd

from datetime import datetime
from logging import getLogger
from pathlib import Path
from time import strftime

from libs.db_handler.src.open_db import load_table, get_latest_db_file
from modules.panel_data.src.year_linker.data_wrangler import wrangle_dataset
from modules.persons.src.common.logger import setup_logging
from modules.persons.src.common.paths import DATA_PATH, PROJECT_ROOT_PATH

logger = getLogger(__name__)


def main(input_path: Path, output_path: Path) -> None:
    df = load_table(input_path, "persons")
    df = wrangle_dataset(df)
    print(input_path)
    with pd.option_context("display.max_columns", None):
        print(df.head())

    df.to_sql("persons", sqlite3.connect(output_path), if_exists="replace", index=False)

    # link_two_years("1920", "1921", df)


if __name__ == "__main__":
    db_dir = DATA_PATH / "output" / "db"
    demo_input_path = get_latest_db_file(db_dir)
    time_stamp = f"{datetime.now():%b %d - %H%M}"
    demo_output_path_db = (
        Path(PROJECT_ROOT_PATH) / "modules" / "panel_data" / "dump" / f"{time_stamp}.db"
    )
    demo_output_path_log = Path(PROJECT_ROOT_PATH) / "modules" / "panel_data" / "dump"

    setup_logging(time_stamp)
    start_time = time.time()

    main(demo_input_path, demo_output_path_db)

    logger.info(
        strftime("Execution time: %M min %S s", time.gmtime(time.time() - start_time))
    )
