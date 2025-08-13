import unittest

from libs.file_handler.src.json.deserializer import deserialize_book_page
from modules.address_books.persons_data_processor.src.models.address_book.address_book_page import (
    AddressBookPage,
)
from modules.address_books.persons_data_processor.src.models.address_book.name_range import (
    NameRange,
)


class MyTestCase(unittest.TestCase):
    def test_valid_input(self):
        test_data = {
            "pdfPageNumber": 1,
            "surnameRange": ["A", "B"],
            "textColumns": {"Spalte01": "Peter Müller", "Spalte02": "Ida Knecht"},
        }

        result = deserialize_book_page(test_data)

        self.assertIsInstance(result, AddressBookPage)
        self.assertEqual(result.pdf_page_number, 1)
        self.assertEqual(result.last_names_range, NameRange("A", "B"))
        self.assertEqual(result.text_content, ["Peter Müller", "Ida Knecht"])

    def test_missing_required_field(self):
        test_data = {
            "pdfPageNumber": 1,
            "surnameRange": ["A", "B"],
            # Missing "textColumns"
        }

        with self.assertRaises(ValueError) as context:
            deserialize_book_page(test_data)
        self.assertIn("is a required property", str(context.exception))
