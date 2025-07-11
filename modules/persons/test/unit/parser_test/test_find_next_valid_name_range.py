import unittest

from modules.persons.src.models.address_book.address_book_page import AddressBookPage
from modules.persons.src.models.address_book.name_range import NameRange
from modules.persons.src.parser.parser import find_next_valid_name_range


class NameRangeTest(unittest.TestCase):
    def test_handle_special_last_names_if_present(self):
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
