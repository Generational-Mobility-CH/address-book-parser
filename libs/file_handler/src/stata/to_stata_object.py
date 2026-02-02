import sqlite3
from pathlib import Path

import pandas as pd
from pandas import DataFrame

from modules.shared.common.paths import OUTPUT_PATH
from modules.shared.constants.table_definition import PERSONS_TABLE_NAME


def to_stata_object(df: DataFrame, output_path: Path) -> None:
    """Transform SQL db into stata object."""
    pass


if __name__ == "__main__":
    db_file = OUTPUT_PATH / "Jan 29 - 1408.db"
    output_path = "stata_file.dta"

    with sqlite3.connect(db_file) as conn:
        query = f"SELECT * FROM {PERSONS_TABLE_NAME}"

        df = pd.read_sql(query, conn)

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = (
            df[col]
            .str.encode("utf-8", errors="ignore")
            .str.decode("utf-8", errors="ignore")
        )

    df.to_stata(output_path, write_index=False)
