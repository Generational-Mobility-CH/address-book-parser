import unittest

from modules.persons_data_processor.src.models.address_book.address_book_page import (
    AddressBookPage,
)
from modules.persons_data_processor.src.models.address_book.name_range import (
    NameRange,
)
from modules.persons_data_processor.src.parser.name_range_handler import (
    find_next_valid_name_range,
    find_next_valid_name_range_start_or_end,
)


class MyTestCase(unittest.TestCase):
    def test_find_next_valid_name_range_start_or_end(self) -> None:
        tc_1 = [
            AddressBookPage(NameRange("Abt", "Abt"), []),
            AddressBookPage(NameRange("Schweizer", "Bankierv"), []),
            AddressBookPage(NameRange("", ""), []),
            AddressBookPage(NameRange("Range", "Invalid"), []),
            AddressBookPage(NameRange("Weber", "Zumstein"), []),
        ]

        tc_2 = [
            AddressBookPage(NameRange("Abt", "Abt"), []),
            AddressBookPage(NameRange("Bach", "Bachmann"), []),
            AddressBookPage(NameRange("Meyer", "müller"), []),
            AddressBookPage(NameRange(" Richard", "Strauss"), []),
            AddressBookPage(NameRange("Schumacher", "Schweizer"), []),
            AddressBookPage(NameRange(" Weber", " Wendelin "), []),
        ]

        test_cases = [
            (tc_1, 0, None),
            (tc_1, 1, None),
            (tc_1, 2, NameRange("Abt", "Weber")),
            (tc_1, len(tc_1) - 1, None),
            (tc_2, 0, None),
            (tc_2, 2, NameRange("Bachmann", "Richard")),
            (tc_2, 3, NameRange("müller", "Schumacher")),
            (tc_2, 4, NameRange("Strauss", "Weber")),
            (tc_2, len(tc_2) - 1, None),
        ]

        for i, (test_input, test_page_index, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_input):
                actual = find_next_valid_name_range(test_input, test_page_index)
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch\nExpected:\t{expected}\nActual:\t\t{actual}",
                )

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
                actual = find_next_valid_name_range_start_or_end(
                    input_collection, page_index, direction
                )
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch: '{actual}' != '{expected}'\nFor input: '{input_collection}'",
                )
