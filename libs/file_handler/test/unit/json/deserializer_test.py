import unittest

from libs.file_handler.src.json.deserializer import deserialize_book_page
from modules.persons.models.address_book.addressBookPage import AddressBookPage


class MyTestCase(unittest.TestCase):
    def test_valid_input(self):
        test_data = {
            "pdfPageNumber": 1,
            "surnameRange": ["A", "B"],
            "textColumns": {"left": "content"},
        }

        result = deserialize_book_page(test_data)

        self.assertIsInstance(result, AddressBookPage)
        self.assertEqual(result.pdf_page_number, 1)
        self.assertEqual(result.surname_range, ["A", "B"])
        self.assertEqual(result.text_columns, {"left": "content"})

    def test_missing_required_field(self):
        test_data = {
            "pdfPageNumber": 1,
            "surnameRange": ["A", "B"],
            # Missing "textColumns"
        }

        with self.assertRaises(ValueError) as context:
            deserialize_book_page(test_data)
        self.assertIn("is a required property", str(context.exception))

    def test_additional_field(self):
        test_data = {
            "pdfPageNumber": 1,
            "surnameRange": ["A", "B"],
            "textColumns": {"left": "content"},
            "extraField": "not allowed",
        }

        with self.assertRaises(ValueError) as context:
            deserialize_book_page(test_data)
        self.assertIn("Additional properties are not allowed", str(context.exception))


if __name__ == "__main__":
    unittest.main()
