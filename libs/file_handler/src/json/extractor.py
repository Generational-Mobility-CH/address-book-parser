import logging
import os

from libs.file_handler.src.models.extractor_strategy import ExtractorStrategy
from libs.file_handler.src.json.deserializer import deserialize_book_page
from libs.file_handler.src.json.reader import read_json
from libs.file_handler.src.util.get_year_from_file_name import get_year_from_file_name
from modules.persons.src.models.address_book.address_book import AddressBook

logger = logging.getLogger(__name__)


class JsonExtractor(ExtractorStrategy):
    def extract(self, data_path: str) -> AddressBook:
        year = get_year_from_file_name(data_path)
        book: AddressBook = AddressBook(year=year, pages=[])

        for file in sorted(os.listdir(data_path)):
            if not file.endswith(".json"):
                logger.info(f"Skipping '{file}'")
                continue

            full_file_path = os.path.join(data_path, file)
            json_data = read_json(full_file_path)

            try:
                book_page = deserialize_book_page(json_data)
            except Exception as e:
                raise ValueError(f"Failed to deserialize address book: {e}")

            book_page.year = year
            book.pages.append(book_page)

        return book
