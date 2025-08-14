import time

from datetime import datetime
from logging import getLogger
from pathlib import Path
from time import strftime
from typing import Optional

from libs.db_handler.src.to_db import save_to_db
from libs.file_handler.src.csv.to_csv import save_to_csv
from libs.file_handler.src.json.extractor import JsonExtractor
from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons_data_processor.src.address_handler.address_cleaner import (
    clean_address,
)
from modules.persons_data_processor.src.common.logger import setup_logging
from modules.persons_data_processor.src.common.paths import (
    PERSONS_OUTPUT_PATH,
    PERSONS_INPUT_PATH,
)
from modules.shared.paths import DATA_PATH
from modules.persons_data_processor.src.constants.database_table_names import (
    PERSONS_ENTRIES_TABLE,
)
from modules.persons_data_processor.src.models.person.person import Person
from modules.persons_data_processor.src.parser.constants.tags import (
    TAG_NONE_FOUND,
)
from modules.persons_data_processor.src.parser.parser import (
    parse_address_book,
)
from modules.persons_data_processor.src.address_handler.street_name_standardizer.street_name_standardizer import (
    standardize_street_name,
)
from modules.persons_data_processor.src.utility.get_subdirectories import (
    get_subdirectories,
)

logger = getLogger(__name__)


def main(
    data_path: Path,
    output_path: Path,
    output_type: SupportedFileTypes = SupportedFileTypes.DB,
    csv_column_names: Optional[list[str]] = None,
) -> None:
    all_paths = get_subdirectories(data_path)
    extractor = JsonExtractor()

    for path in all_paths:
        book = extractor.extract(path)  # TODO: use functional programming style
        book = parse_address_book(book)
        for person in book:
            person.address = clean_address(person.address)
            person.address.street_name = standardize_street_name(
                person.address.street_name
            )

        save_persons(book, output_path, output_type, csv_column_names)


# TODO: put this in another module
def save_persons(
    persons: list[Person],
    output_path: Path,
    output_type: SupportedFileTypes,
    csv_column_names: Optional[list[str]] = None,
):
    match output_type:
        case SupportedFileTypes.DB:
            save_to_db(persons, output_path, PERSONS_ENTRIES_TABLE)
        case SupportedFileTypes.CSV:
            save_to_csv(persons, output_path, csv_column_names)

    year = persons[0].year if persons else TAG_NONE_FOUND

    logger.info(
        f"Saved persons from year '{year}' to '{output_type.value}' at '{output_path}'"
    )


if __name__ == "__main__":
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    demo_output_type = SupportedFileTypes.DB.value
    time_stamp = f"{datetime.now():%b %d - %H%M}"
    demo_output_path = (
        Path(PERSONS_OUTPUT_PATH)
        / demo_output_type
        / f"{time_stamp}.{demo_output_type}"
    )

    setup_logging(time_stamp, PERSONS_OUTPUT_PATH / "logs")
    start_time = time.time()

    main(PERSONS_INPUT_PATH, demo_output_path)

    logger.info(
        strftime("Execution time: %M min %S s", time.gmtime(time.time() - start_time))
    )
