import unittest

from modules.persons.src.standardizer.street_name_standardizer import (
    standardize_street_name,
)


class StreetNameStandardizerTestCase(unittest.TestCase):
    def test_standardize_street_name(self) -> None:
        test_cases = [
            ("Bahnhofstr.", "Bahnhofstrasse"),
            ("Albanthal.", "Albanthal"),
            ("Totengässl.", "Totengässlein"),
            ("Unt. Rebg.", "TODO"),
            ("Müllerw.", "Müllerweg"),
            ("Claragr.", "Claragraben"),
            ("Kohlenbergg.", "Kohlenbergg"),
            ("Breite..", "Breite"),
            ("Kembserweg.", "Kembserweg"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                input_str = standardize_street_name(input_str)

                actual = input_str
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
