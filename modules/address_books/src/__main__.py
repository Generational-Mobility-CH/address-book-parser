from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Optional

from libs.file_handler.src.json.extractor import JsonExtractor
from modules.address_books.src.address_handler.address_cleaner import (
    clean_address,
)
from modules.address_books.src.address_handler.street_name_standardizer.street_name_standardizer import (
    standardize_street_name,
)
from modules.address_books.src.common.paths import (
    ADDRESS_BOOK_ENTRIES_OUTPUT_PATH,
    ADDRESS_BOOKS_INPUT_PATH,
)
from modules.address_books.src.parser.constants.tags import (
    TAG_NONE_FOUND,
)
from modules.address_books.src.parser.parser import (
    parse_address_book,
)
from modules.address_books.src.repository.get_repository import (
    get_person_repository,
)
from modules.shared.repository.supported_file_types import (
    SupportedFileTypes,
)
from modules.address_books.src.setup import setup
from modules.address_books.src.utility.get_subdirectories import (
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
    repository = get_person_repository(output_type, csv_column_names)

    for path in all_paths:
        book = extractor.extract(path)  # TODO: use functional programming style
        book = parse_address_book(book)
        for person in book:
            person.address = clean_address(person.address)
            person.address.street_name = standardize_street_name(
                person.address.street_name
            )

        repository.save(book, output_path)
        year = book[0].year if book else TAG_NONE_FOUND
        logger.info(
            f"Saved persons from year '{year}' to '{output_type.value}' at '{output_path}'"
        )


if __name__ == "__main__":
    demo_output_type = SupportedFileTypes.DB
    time_stamp = f"{datetime.now():%b %d - %H%M}"
    demo_output_path = (
        ADDRESS_BOOK_ENTRIES_OUTPUT_PATH
        / demo_output_type.value
        / f"{time_stamp}.{demo_output_type.value}"
    )

    setup(time_stamp)

    main(ADDRESS_BOOKS_INPUT_PATH, demo_output_path, demo_output_type)
