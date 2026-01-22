from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Optional

from libs.file_handler.src.json.extractor import JsonExtractor
from modules.repository.src.constants.db_column_names import DB_COLUMN_NAMES
from modules.repository.src.get_repository import get_person_repository
from modules.repository.src.panel_data_repository import PanelDataRepository
from modules.repository.src.supported_file_types import (
    SupportedFileTypes,
)
from modules.repository.src.utility.get_latest_db_file import (
    get_latest_db_file,
)
from modules.repository.src.utility.get_table_entries import (
    get_table_entries,
)
from modules.setup import setup
from modules.shared.common.paths import (
    ADDRESS_BOOK_ENTRIES_OUTPUT_PATH,
    PANEL_DATA_INPUT_PATH,
    PANEL_DATA_OUTPUT_PATH,
)
from modules.shared.constants.database_table_names import PERSONS_ENTRIES_TABLE_NAME
from modules.shared.constants.paths import DATA_PATH
from modules.shared.constants.years_range import YEARS_RANGE
from modules.shared.models.address import Address
from modules.shared.models.address_book.address_book_entry import AddressBookEntry
from modules.shared.models.panel_data_entry import PanelDataEntry
from modules.text_cleaner.src.address_cleaner import (
    clean_address,
)
from modules.text_parser.src.gender_identifier import identify_gender
from modules.text_parser.src.parser import (
    parse_address_book,
)
from modules.text_parser.src.separator.separator import (
    separate_partner,
    separate_information,
)
from modules.text_standardizer.src.standardizer import standardize_information
from modules.text_standardizer.src.street_name_standardizer import (
    standardize_street_name,
)

_logger = getLogger(__name__)


def create_address_books_db(
    data_path: Path,
    output_path: Path,
    output_type: SupportedFileTypes = SupportedFileTypes.DB,
    csv_column_names: Optional[list[str]] = None,
) -> None:
    _logger.info("Started creation of the address books database...")
    book_paths = [entry for entry in data_path.iterdir() if entry.is_dir()]
    extractor = JsonExtractor()
    repository = get_person_repository(output_type, csv_column_names)

    for path in book_paths:
        book = extractor.extract(path)
        persons_entries = parse_address_book(book)
        for person in persons_entries:
            person.address = clean_address(person.address)
            person.address.street_name = standardize_street_name(
                person.address.street_name
            )

        repository.save(persons_entries, output_path)


def create_panel_data_db(input_path: Path, output_path: Path) -> None:
    _logger.info(f"Reading data from {input_path} ...")

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

        if address_book_entries:
            panel_data = parse_panel_data_set(address_book_entries)
            PanelDataRepository().save(panel_data, output_path)


def parse_panel_data_set(
    address_book_entries: list[AddressBookEntry],
) -> list[PanelDataEntry]:
    _logger.info(f"Parsing persons from year {address_book_entries[0].year} ...")

    separated_entries = separate_information(address_book_entries)

    gendered_entries_first_run = identify_gender(separated_entries)
    standardized_entries_first_run = standardize_information(gendered_entries_first_run)
    gendered_entries = identify_gender(standardized_entries_first_run)
    standardized_entries = standardize_information(gendered_entries)

    result = separate_partner(standardized_entries)

    return result


if __name__ == "__main__":
    time_stamp = f"{datetime.now():%b %d - %H%M}"
    setup(
        time_stamp,
        [
            DATA_PATH,
            ADDRESS_BOOK_ENTRIES_OUTPUT_PATH,
            PANEL_DATA_OUTPUT_PATH,
            PANEL_DATA_OUTPUT_PATH / "db",
        ],
    )

    # create_address_books_db(
    #     ADDRESS_BOOKS_INPUT_PATH,
    #     ADDRESS_BOOK_ENTRIES_OUTPUT_PATH / "db" / f"{time_stamp}.db",
    # )

    create_panel_data_db(
        get_latest_db_file(PANEL_DATA_INPUT_PATH),
        PANEL_DATA_OUTPUT_PATH / "db" / f"{time_stamp}.db",
    )
