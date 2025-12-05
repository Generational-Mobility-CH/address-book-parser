import re
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from modules.address_books.src.constants.table_definition import (
    PERSONS_TABLE_NAME,
    PERSONS_TABLE_COLUMNS_DECLARATION,
)
from modules.shared.constants.paths import DATA_PATH


def save_data(data: DataFrame, output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(output_path) as connection:
        connection.execute(
            f"CREATE TABLE IF NOT EXISTS {PERSONS_TABLE_NAME}({PERSONS_TABLE_COLUMNS_DECLARATION})"
        )
        data.to_sql(PERSONS_TABLE_NAME, connection, if_exists="append", index=False)


if __name__ == "__main__":
    input_dir = DATA_PATH / "test" / "transcriptions" / "persons"
    output_dir = DATA_PATH / "test" / "db" / f"Basel-{datetime.now():%b %d - %H%M}.db"

    for book in input_dir.iterdir():
        year_match = re.search(r"\d{4}$", book.name)
        if book.is_dir() and year_match:
            year = year_match.group(0)
            for page in book.iterdir():
                page_data = pd.read_csv(page)
                page_data["year"] = year
                page_data["page_number"] = page.stem
                # page_data["original_entry"] = page_data.apply(
                #     lambda row: f"{row['last_name']} {row['partner_last_name']} {row['first_names']}, {row['street_name']} {row['house_number']}, {row['job']}",
                #     axis=1,
                # )

                save_data(page_data, output_dir)
