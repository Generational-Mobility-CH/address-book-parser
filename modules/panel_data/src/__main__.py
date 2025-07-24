from pathlib import Path

from libs.db_handler.src.open_db import load_table, get_latest_db_file
from modules.panel_data.src.year_linker.year_linker import link_two_years
from modules.persons.src.common.paths import DATA_PATH


def main(data_path: Path) -> None:
    df = load_table(data_path, "persons")
    print(df.head())
    link_two_years("1920", "1921", df)


if __name__ == "__main__":
    db_dir = DATA_PATH / "output" / "db"
    latest_db_path = get_latest_db_file(db_dir)
    main(latest_db_path)
