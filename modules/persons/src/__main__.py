import logging
from datetime import datetime

from libs.db_handler.src.to_db import save_to_db
from libs.file_handler.src.csv.to_csv import save_to_csv
from libs.file_handler.src.extractor import extract_data
from modules.persons.common.logger import setup_logging
from modules.persons.common.paths import OUTPUT_PATH, INPUT_PATH
from modules.persons.src.parser.parser import parse_address_book


logger = logging.getLogger(__name__)


def main(data_path: str, output_path: str) -> None:
    all_books = extract_data(data_path)

    persons_collection = []
    for book in all_books:
        persons_collection.extend(parse_address_book(book))

    cleaned_persons = [person.standardize_attributes() for person in persons_collection]
    save_to_db(cleaned_persons, output_path)


if __name__ == "__main__":
    setup_logging()
    demo_input_path = f"{INPUT_PATH}/json"
    demo_output_path = f"{OUTPUT_PATH}/db/{datetime.now():%m.%d-%H.%M.%S}.db"
    main(demo_input_path, demo_output_path)
