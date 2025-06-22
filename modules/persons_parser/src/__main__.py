import logging

from libs.file_handler.src.extractor import extract_data
from modules.common.paths import DATA_PATH, OUTPUT_PATH, INPUT_PATH
from modules.persons_parser.src.load.loader import save_data, OutputFileType
from modules.persons_parser.src.parser.parser import parse_address_book


logger = logging.getLogger(__name__)


def main(data_path: str, output_path: str) -> None:
    all_books = extract_data(data_path)

    for book in all_books:
        persons = parse_address_book(book)
        save_data(persons, f"{output_path}/{book.year}.csv", OutputFileType.CSV)


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s-%(name)s-%(levelname)s: %(message)s',
        datefmt='%Y.%m.%d %H:%M',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{DATA_PATH}/app.log')
        ]
    )


if __name__ == "__main__":
    setup_logging()
    demo_data_path = f"{INPUT_PATH}/json"
    demo_output_path = f"{OUTPUT_PATH}/csv"
    main(demo_data_path, demo_output_path)
