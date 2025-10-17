from datetime import datetime
from logging import getLogger
from pathlib import Path

from modules.panel_data.src.repository.utility.get_table_entries import (
    get_table_entries,
)
from modules.panel_data.src.repository.utility.get_latest_db_file import (
    get_latest_db_file,
)
from modules.panel_data.src.constants.paths import (
    PANEL_DATA_OUTPUT_PATH,
    PANEL_DATA_INPUT_PATH,
)
from modules.panel_data.src.gender_calculator.gender_calculator import identify_females
from modules.panel_data.src.models.panel_data_entry import PanelDataEntry
from modules.panel_data.src.repository.panel_data_repository import PanelDataRepository
from modules.panel_data.src.separator.separator import separate_information
from modules.panel_data.src.setup import setup
from modules.address_books.src.constants.database_table_names import (
    PERSONS_ENTRIES_TABLE_NAME,
)
from modules.address_books.src.models.address import Address
from modules.address_books.src.models.address_book.address_book_entry import (
    AddressBookEntry,
)
from modules.address_books.src.repository.constants.db_column_names import (
    DB_COLUMN_NAMES,
)
from modules.shared.constants.years_range import YEARS_RANGE

logger = getLogger(__name__)


def main(input_path: Path, output_path: Path) -> None:
    logger.info(f"Reading data from {input_path}")

    for year in YEARS_RANGE:
        entries = get_table_entries(
            input_path, PERSONS_ENTRIES_TABLE_NAME, f" WHERE year LIKE {year}"
        )

        address_book_entries = []
        for row in entries:
            entry_data = dict(zip(DB_COLUMN_NAMES, row))
            address = Address(
                street_name=entry_data.pop("street_name"),
                house_number=entry_data.pop("house_number"),
            )
            entry = AddressBookEntry(address=address, **entry_data)
            address_book_entries.append(entry)

        logger.info(f"Parsing persons from year {year}")
        panel_data = parse_panel_data_set(address_book_entries, output_path)

        PanelDataRepository().save(panel_data, output_path)
        logger.info(f"Saved persons to '{output_path}'")


def parse_panel_data_set(
    address_book_entries: list[AddressBookEntry], db_path: Path
) -> list[PanelDataEntry]:
    panel_data_entries = separate_information(address_book_entries)
    panel_data_entries = identify_females(panel_data_entries, db_path)
    # persons = standardize_information(persons)

    return panel_data_entries


if __name__ == "__main__":
    demo_input_path = get_latest_db_file(PANEL_DATA_INPUT_PATH)
    time_stamp = f"{datetime.now():%b %d - %H%M%S}"
    demo_output_path = PANEL_DATA_OUTPUT_PATH / "db" / f"{time_stamp}.db"

    setup(time_stamp)
    main(demo_input_path, demo_output_path)
