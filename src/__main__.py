from datetime import datetime
from logging import getLogger
from pathlib import Path
from typing import Optional

from src.file_handler.src.json.extractor import JsonExtractor
from src.repository.src.constants.table_definitions import (
    COMPANIES_TABLE_NAME,
)
from src.repository.src.csv_repository import CsvRepository
from src.repository.src.db_repository import DbRepository
from src.repository.src.get_repository import get_person_repository
from src.repository.src.supported_file_types import (
    SupportedFileTypes,
)
from src.setup import setup
from src.shared.common.paths import (
    OUTPUT_PATH,
    INPUT_PATH,
    DATA_PATH,
    CITY,
)
from src.text_parser.src.address_parser import add_coordinates
from src.text_parser.src.gender_identifier import identify_gender
from src.text_parser.src.parser import (
    parse_address_book,
)
from src.text_standardizer.src.standardizer import standardize_information
from src.text_standardizer.src.street_name_standardizer import standardize_street_name

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
    if output_type == SupportedFileTypes.DB:
        company_repository = DbRepository(table_name=COMPANIES_TABLE_NAME)
    else:
        company_repository = CsvRepository(csv_column_names)
    book_paths = [entry for entry in input_path.iterdir() if entry.is_dir()]

    for path in book_paths:
        book = extractor.extract(path)
        panel_data, companies = parse_address_book(book)

        # TODO: find cleaner solution - some job/name standardization depends on the gender, but the gender is also identified via job/name ...
        panel_data = identify_gender(panel_data)
        panel_data = standardize_information(panel_data)
        panel_data = identify_gender(panel_data)
        panel_data = standardize_information(panel_data)
        for person in panel_data:
            person.address = add_coordinates(person.address)

        repository.save(panel_data, output_path)

        # Company postprocessing: standardize streets and geocode
        for company in companies:
            company.address.street_name = standardize_street_name(
                company.address.street_name
            )
            company.address = add_coordinates(company.address)

        if companies:
            if output_type == SupportedFileTypes.CSV:
                company_output = output_path.with_stem(
                    output_path.stem + "_companies"
                )
            else:
                company_output = output_path
            company_repository.save(companies, company_output)

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

    main(INPUT_PATH, OUTPUT_PATH / f"ALL_BOOKS-{CITY}.db")
