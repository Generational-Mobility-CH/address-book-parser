import logging
from datetime import datetime

from libs.db_handler.src.to_db import save_to_db
from libs.file_handler.src.csv.to_csv import save_to_csv
from libs.file_handler.src.extractor import extract_data
from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.common.logger import setup_logging
from modules.persons.common.paths import OUTPUT_PATH, INPUT_PATH
from modules.persons.src.parser.parser import parse_address_book


logger = logging.getLogger(__name__)


def main(
    data_path: str,
    output_path: str,
    output_type: SupportedFileTypes = SupportedFileTypes.DB,
) -> None:
    address_books = extract_data(data_path)
    raw_persons = [
        person for book in address_books for person in parse_address_book(book)
    ]
    standardized_persons = [p.standardize_attributes() for p in raw_persons]

    match output_type:
        case SupportedFileTypes.DB:
            logger.info(f"Saving persons to database at {output_path}")
            save_to_db(standardized_persons, output_path)
        case SupportedFileTypes.CSV:
            logger.info(f"Saving persons to .csv at {output_path}")
            save_to_csv(standardized_persons, output_path)


if __name__ == "__main__":
    setup_logging()
    demo_output_type = SupportedFileTypes.DB
    demo_input_path = f"{INPUT_PATH}/json"
    demo_output_path = f"{OUTPUT_PATH}/{demo_output_type.value}/{datetime.now():%m.%d-%H.%M.%S}.{demo_output_type.value}"
    main(demo_input_path, demo_output_path)
