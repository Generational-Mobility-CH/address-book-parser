import logging
import os
import time

from datetime import datetime

from libs.db_handler.src.to_db import save_to_db
from libs.file_handler.src.csv.to_csv import save_to_csv
from libs.file_handler.src.json.extractor import JsonExtractor
from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.common import setup_logging
from modules.persons.src.common import OUTPUT_PATH, INPUT_PATH
from modules.persons.src.parser.parser import parse_address_book


logger = logging.getLogger(__name__)


def main(
    data_path: str,
    output_path: str,
    output_type: SupportedFileTypes = SupportedFileTypes.DB,
) -> None:
    start_time = time.time()
    extractor = JsonExtractor()
    all_paths = get_all_data_paths(data_path)

    for path in all_paths:
        book = extractor.extract(path)
        raw_persons = parse_address_book(book)
        standardized_persons = [p.standardize_attributes() for p in raw_persons]

        match output_type:
            case SupportedFileTypes.DB:
                save_to_db(standardized_persons, output_path)
            case SupportedFileTypes.CSV:
                save_to_csv(standardized_persons, output_path)

        logger.info(f"Saved persons to {output_type.value} at {output_path}")

    elapsed = time.time() - start_time
    logger.info(f"Execution time: {elapsed:.2f} seconds")


def get_all_data_paths(base_path: str) -> list[str]:
    result = []
    for folder in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, folder)):
            result.append(os.path.join(base_path, folder))
    return result


if __name__ == "__main__":
    setup_logging()
    demo_output_type = SupportedFileTypes.DB
    demo_input_path = f"{INPUT_PATH}/json"
    demo_output_path = f"{OUTPUT_PATH}/{demo_output_type.value}/{datetime.now():%m.%d-%H.%M.%S}.{demo_output_type.value}"
    main(demo_input_path, demo_output_path)
