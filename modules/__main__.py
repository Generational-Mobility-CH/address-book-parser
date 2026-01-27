from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Optional

from libs.file_handler.src.json.extractor import JsonExtractor
from modules.repository.src.get_repository import get_person_repository
from modules.repository.src.supported_file_types import (
    SupportedFileTypes,
)
from modules.setup import setup
from modules.shared.common.paths import (
    OUTPUT_PATH,
    INPUT_PATH,
    DATA_PATH,
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

_logger = getLogger(__name__)


def main(
    input_path: Path,
    output_path: Path,
    output_type: SupportedFileTypes = SupportedFileTypes.DB,
    csv_column_names: Optional[list[str]] = None,
) -> None:
    _logger.info("Started creation of the address books database...")

    extractor = JsonExtractor()
    repository = get_person_repository(output_type, csv_column_names)
    book_paths = [entry for entry in input_path.iterdir() if entry.is_dir()]

    for path in book_paths:
        book = extractor.extract(path)
        persons_entries = parse_address_book(book)

        panel_data = separate_information(persons_entries)  # TODO: put this in parser

        # TODO: find cleaner solution - some job/name standardization depends on the gender, but the gender is also identified via job/name ...
        panel_data = identify_gender(panel_data)
        panel_data = standardize_information(panel_data)
        panel_data = identify_gender(panel_data)
        panel_data = standardize_information(panel_data)

        panel_data = separate_partner(panel_data)  # TODO: put this in parser

        repository.save(panel_data, output_path)

    _logger.info("Finished creation of the address books database.")


if __name__ == "__main__":
    time_stamp = f"{datetime.now():%b %d - %H%M}"

    setup(
        time_stamp,
        [
            DATA_PATH,
            INPUT_PATH,
            OUTPUT_PATH,
        ],
    )

    main(INPUT_PATH, OUTPUT_PATH / f"{time_stamp}.db")
