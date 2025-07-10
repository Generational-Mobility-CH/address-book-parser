import os
import time

from datetime import datetime
from logging import getLogger
from pathlib import Path
from time import strftime

from libs.db_handler.src.to_db import save_to_db
from libs.file_handler.src.csv.to_csv import save_to_csv
from libs.file_handler.src.json.extractor import JsonExtractor
from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.cleaner.cleaner import clean_person
from modules.persons.src.common.logger import setup_logging
from modules.persons.src.common.paths import INPUT_PATH, OUTPUT_PATH, DATA_PATH
from modules.persons.src.parser.parser import parse_address_book


logger = getLogger(__name__)


def main(
    data_path: str,
    output_path: str,
    output_type: SupportedFileTypes = SupportedFileTypes.DB,
    csv_column_names: list[str] = None,
) -> None:
    extractor = JsonExtractor()
    all_paths = get_all_data_paths(data_path)

    for path in all_paths:
        book = extractor.extract(path)
        raw_persons = parse_address_book(book)
        cleaned_persons = [clean_person(p) for p in raw_persons]
        standardized_persons = [p.standardize_attributes() for p in cleaned_persons]

        match output_type:
            case SupportedFileTypes.DB:
                save_to_db(standardized_persons, output_path)
            case SupportedFileTypes.CSV:
                save_to_csv(standardized_persons, output_path, csv_column_names)

        logger.info(
            f"Saved persons from year '{book.year}' to {output_type.value} at {output_path}"
        )


def get_all_data_paths(base_path: str) -> list[str]:
    result = []

    for folder in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, folder)):
            result.append(os.path.join(base_path, folder))

    return result


if __name__ == "__main__":
    demo_output_type = SupportedFileTypes.DB
    Path(DATA_PATH).mkdir(parents=True, exist_ok=True)
    demo_input_path = f"{INPUT_PATH}/json"
    time_stamp = f"{datetime.now():%b %d. - %H.%M}"
    demo_output_path = (
        f"{OUTPUT_PATH}/{demo_output_type.value}/{time_stamp}.{demo_output_type.value}"
    )

    setup_logging(time_stamp)
    start_time = time.time()

    main(demo_input_path, demo_output_path)

    logger.info(
        strftime("Execution time: %M min %S s", time.gmtime(time.time() - start_time))
    )
