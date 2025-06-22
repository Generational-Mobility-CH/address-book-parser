import logging
import os
import re

from libs.file_handler.src.extractor_strategy import ExtractorStrategy
from libs.file_handler.src.json.deserializer import deserialize_book_page
from libs.file_handler.src.json.reader import read_json
from modules.models.addressBook import AddressBook

logger = logging.getLogger(__name__)


class JsonExtractor(ExtractorStrategy):
    def extract(self, data_paths: list[str]) -> list[AddressBook]:
        books_collection: list[AddressBook] = []

        for sub_folder_path in data_paths:
            if os.path.isdir(sub_folder_path):
                year = 0
                try:
                    year = int(get_year_from_file_name(os.path.basename(sub_folder_path)))
                except Exception as e:
                    logger.warning(f"Failed to extract year from {sub_folder_path}: {e}")

                book: AddressBook = AddressBook(year=year, pages=[])

                for file in sorted(os.listdir(sub_folder_path)):
                    if not file.endswith('.json'):
                        logger.info(f"Skipping '{file}'")
                        continue
                    file_path = os.path.join(sub_folder_path, file)
                    json_data = read_json(file_path)
                    try:
                        book_page = deserialize_book_page(json_data)
                    except Exception as e:
                        raise ValueError(f"Failed to deserialize address book: {e}")
                    book.pages.append(book_page)
                books_collection.append(book)
            else:
                one_book: AddressBook = AddressBook(year=0, pages=[])
                json_data = read_json(data_paths[0])
                try:
                    book_page = deserialize_book_page(json_data)
                except Exception as e:
                    raise ValueError(f"Failed to deserialize address book: {e}")
                one_book.pages.append(book_page)
                books_collection.append(one_book)

        return books_collection


def get_year_from_file_name(file_name: str) -> str:
        match = re.search(r'([19|20]\d{3})', file_name)
        return match.group(0) if match else "0"
