import unittest

from modules.persons.src.standardizer.street_name_standardizer.street_name_standardizer import (
    standardize_street_name,
)


class StreetNameStandardizerTestCase(unittest.TestCase):
    def test_standardize_street_name(self) -> None:
        test_cases = [
            ("Bahnhofstr.", "Bahnhofstrasse"),
            ("Totengässl.", "Totengässlein"),
            ("Bernerring", "Bernerring"),
            ("Claragr.", "Claragraben"),
            ("Kembserweg.", "Kembserweg"),
            ("Kanoneng.", "Kanonengasse"),
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

    def test_correct_street_name_spelling(self) -> None:
        test_cases = [
            ("Pfrtergasse", "Pfirtergasse"),
            ("Thierst-Allee", "Thiersteinerallee"),
            ("Johannsring", "St. Johanns-Ring"),
            ("Albantal", "St. Alban-Tal"),
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

    # def test_standardize_multi_part_street_names(self) -> None:
    #     test_cases = [
    #         ("Unt. Rebg.", "TODO"),
    #     ]
    #
    #     for i, (input_str, expected) in enumerate(test_cases):
    #         with self.subTest(i=i, input=input_str):
    #             input_str = standardize_street_name(input_str)
    #
    #             actual = input_str
    #             self.assertEqual(
    #                 actual,
    #                 expected,
    #                 f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
    #             )
