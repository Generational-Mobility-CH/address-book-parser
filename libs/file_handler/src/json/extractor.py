import logging
from pathlib import Path

from libs.file_handler.src.models.extractor_strategy import ExtractorStrategy
from libs.file_handler.src.json.deserializer import deserialize_book_page
from libs.file_handler.src.json.reader import read_json
from libs.file_handler.src.util.get_year_from_file_name import get_year_from_file_name
from modules.persons.src.models.address_book.address_book import AddressBook

logger = logging.getLogger(__name__)


class JsonExtractor(ExtractorStrategy):
    def extract(self, data_path: Path) -> AddressBook:
        year = get_year_from_file_name(data_path)
        book: AddressBook = AddressBook(year=year, pages=[])

        for file_path in sorted(data_path.iterdir()):
            if file_path.suffix != ".json":
                logger.info(f"Skipping '{file_path.name}'")
                continue

            json_data = read_json(file_path)

            try:
                book_page = deserialize_book_page(json_data)
            except Exception as e:
                raise ValueError(f"Failed to deserialize address book: {e}")

            if book_page.text_content:
                book_page.year = year
                book.pages.append(book_page)

        return book
