import unittest

from modules.persons_data_processor.src.address_handler.street_name_standardizer.street_name_standardizer import (
    standardize_street_name,
)


class StreetNameStandardizerTestCase(unittest.TestCase):
    def test_standardize_street_name(self) -> None:
        test_cases = [
            ("Bahnhofstr.", "Bahnhofstrasse"),
            ("Bahnhofstr", "Bahnhofstrasse"),
            ("Totengässl.", "Totengässlein"),
            ("Bernerring", "Bernerring"),
            ("Claragr.", "Claragraben"),
            ("Kembserweg.", "Kembserweg"),
            ("Kanoneng.", "Kanonengasse"),
            ("Kanonengasse", "Kanonengasse"),
            ("Feldbergstr", "Feldbergstrasse"),
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
