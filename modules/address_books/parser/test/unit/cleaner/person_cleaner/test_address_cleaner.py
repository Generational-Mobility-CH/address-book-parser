import unittest

from modules.address_books.parser.src.cleaner.address_cleaner import clean_address
from modules.address_books.parser.src.models.person.address import Address


class CleanAddressTestCase(unittest.TestCase):
    def test_clean_address(self) -> None:
        test_cases = [
            (Address(". 100Amerbachstr", ""), Address("Amerbachstr", "100")),
            (Address(".100Amerbachstr", ""), Address("Amerbachstr", "100")),
            (Address(". 100 Amerbachstr", ""), Address("Amerbachstr", "100")),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = clean_address(test_input)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )

    def test_clean_parenthesis_in_address(self) -> None:
        test_cases = [
            (Address("Jakobstr (36 Gundloldingerstr)", "1"), Address("Jakobstr", "1")),
            (Address("(1. OG)  Amerbachstr", "1"), Address("Amerbachstr", "1")),
            (Address("Amerbachstr (1. OG)", "1"), Address("Amerbachstr", "1")),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = clean_address(test_input)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )

    def test_get_street_name_from_house_nr(self):
        test_cases = [
            (Address("", "40Wiesenschanzweg"), Address("Wiesenschanzweg", "40")),
            (Address("", "14Byfangweg"), Address("Byfangweg", "14")),
            (Address("", "28Rebgasse"), Address("Rebgasse", "28")),
            (Address("", "28"), Address("", "28")),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = clean_address(test_input)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
