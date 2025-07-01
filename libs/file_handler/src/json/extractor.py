import logging
import os
import re

from libs.file_handler.src.models.extractor_strategy import ExtractorStrategy
from libs.file_handler.src.json.deserializer import deserialize_book_page
from libs.file_handler.src.json.reader import read_json
from modules.persons.src.models.address_book import AddressBook


logger = logging.getLogger(__name__)


class JsonExtractor(ExtractorStrategy):
    def extract(self, data_path: str) -> AddressBook:
        year = get_year_from_file_name(data_path)
        book: AddressBook = AddressBook(year=int(year), pages=[])

        for file in sorted(os.listdir(data_path)):
            if not file.endswith(".json"):
                logger.info(f"Skipping '{file}'")
                continue

            full_file_path = os.path.join(data_path, file)
            json_data = read_json(full_file_path)

            try:
                book_page = deserialize_book_page(json_data)
            except Exception as e:
                raise ValueError(f"Failed to deserialize address book: {e.__str__()}")

            book.pages.append(book_page)

        return book


def get_year_from_file_name(file_name: str) -> str:
    match = re.search(r"([19|20]\d{3})", file_name)
    return match.group(0) if match else "0"
