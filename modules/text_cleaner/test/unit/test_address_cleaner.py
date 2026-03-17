import unittest

from modules.text_cleaner.src.address_cleaner import (
    clean_address,
)
from modules.shared.models.address import Address


class CleanAddressTestCase(unittest.TestCase):
    def test_clean_address(self) -> None:
        test_cases = [
            (
                Address(". 100Amerbachstr", "", coordinates=None),
                Address("Amerbachstr", "100", coordinates=None),
            ),
            (
                Address(".100Amerbachstr", "", coordinates=None),
                Address("Amerbachstr", "100", coordinates=None),
            ),
            (
                Address(". 100 Amerbachstr", "", coordinates=None),
                Address("Amerbachstr", "100", coordinates=None),
            ),
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
            (
                Address("Jakobstr (36 Gundloldingerstr)", "1", coordinates=None),
                Address("Jakobstr", "1", coordinates=None),
            ),
            (
                Address("(1. OG)  Amerbachstr", "1", coordinates=None),
                Address("Amerbachstr", "1", coordinates=None),
            ),
            (
                Address("Amerbachstr (1. OG)", "1", coordinates=None),
                Address("Amerbachstr", "1", coordinates=None),
            ),
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
            (
                Address("", "40Wiesenschanzweg", coordinates=None),
                Address("Wiesenschanzweg", "40", coordinates=None),
            ),
            (
                Address("", "14Byfangweg", coordinates=None),
                Address("Byfangweg", "14", coordinates=None),
            ),
            (
                Address("", "28Rebgasse", coordinates=None),
                Address("Rebgasse", "28", coordinates=None),
            ),
            (Address("", "28", coordinates=None), Address("", "28", coordinates=None)),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = clean_address(test_input)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
