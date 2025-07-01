import unittest

from modules.persons.src.models.address_book.address_book_page import AddressBookPage
from modules.persons.src.models.address_book.name_range import NameRange
from modules.persons.src.parser.parser import get_next_valid_name_range


class NameRangeTest(unittest.TestCase):
    def test_find_next_valid_name_range(self) -> None:
        test_cases = [
            # Forward search finds first valid
            (
                [
                    AddressBookPage(NameRange("", ""), text_content={}),
                    AddressBookPage(NameRange("Abt", "Bachmann"), text_content={}),
                    AddressBookPage(NameRange("Bachmann", "Christen"), text_content={}),
                ],
                1,
                1,
                "Abt",
            ),
            # Forward search finds next valid
            (
                [
                    AddressBookPage(NameRange("Abt", "Bachmann"), text_content={}),
                    AddressBookPage(NameRange("Bachmann", "Christen"), text_content={}),
                    AddressBookPage(NameRange("Euler", "Färber"), text_content={}),
                    AddressBookPage(NameRange("", ""), text_content={}),
                    AddressBookPage(NameRange("", ""), text_content={}),
                    AddressBookPage(NameRange("", ""), text_content={}),
                    AddressBookPage(NameRange("", ""), text_content={}),
                ],
                5,
                -1,
                "Färber",
            ),
            # Backward search finds first valid
            (
                [
                    AddressBookPage(NameRange("Abt", "Bachmann"), text_content={}),
                    AddressBookPage(
                        NameRange("Christen", "Diffie-Hellman"), text_content={}
                    ),
                    AddressBookPage(NameRange("", ""), text_content={}),
                ],
                2,
                -1,
                "Diffie-Hellman",
            ),
            # Backward search finds next valid
            (
                [
                    AddressBookPage(NameRange("Abt", "Bachmann"), text_content={}),
                    AddressBookPage(NameRange("Christen", ""), text_content={}),
                    AddressBookPage(NameRange("", ""), text_content={}),
                ],
                2,
                -1,
                "Bachmann",
            ),
            # Return empty string if no valid name range found
            (
                [AddressBookPage(NameRange("", ""), text_content={})],
                0,
                1,
                "",
            ),
            # Index out of bounds
            (
                [],
                1,
                1,
                "",
            ),
            # Index out of bounds
            (
                [AddressBookPage(NameRange("Abt", "Bachmann"), text_content={})],
                1,
                1,
                "",
            ),
        ]

        for i, (input_collection, page_index, direction, expected) in enumerate(
            test_cases
        ):
            with self.subTest(i=i, input=input_collection):
                actual = get_next_valid_name_range(
                    input_collection, page_index, direction
                )
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch: '{actual}' != '{expected}'\nFor input: '{input_collection}'",
                )
