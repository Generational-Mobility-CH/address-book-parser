import unittest

from modules.persons_data_processor.src.address_handler.street_name_standardizer.street_name_standardizer import (
    standardize_street_name,
)


class StreetNameSuffixStandardizationTest(unittest.TestCase):
    def test_standardize_multi_part_street_names(self) -> None:
        test_cases = [
            ("Unt. Rebg.", "Untere Rebgasse"),
            ("Untere Rebg.", "Untere Rebgasse"),
            ("Untere Rebgasse", "Untere Rebgasse"),
            ("Obere Wenkenhofstr.", "Obere Wenkenhofstrasse"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = standardize_street_name(input_str)

                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
