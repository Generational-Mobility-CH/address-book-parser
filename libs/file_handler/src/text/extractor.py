from libs.file_handler.src.models.extractor_strategy import ExtractorStrategy
from libs.file_handler.src.text.reader import read_text
from modules.persons.models.addressBook import AddressBook
from modules.persons.models.addressBookPage import AddressBookPage


class TextExtractor(ExtractorStrategy):
    def extract(self, data_paths: list[str]) -> list[AddressBook]:
        """
        Legacy support for text files that contain the relevant addresses in 1 file.
        In this case, the resulting extract() output contains 1 AddressBookPage
        with 1 column containing the whole text.
        """
        books_collection = []

        for path in data_paths:
            content = read_text(path)
            page = AddressBookPage(surname_range=[], text_columns={"Spalte01": content})
            book = AddressBook(year=0, pages=[page])
            books_collection.append(book)

        return books_collection
