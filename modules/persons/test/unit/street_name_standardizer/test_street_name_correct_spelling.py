import unittest

from modules.persons.src.street_name_standardizer.street_name_standardizer import (
    standardize_street_name,
)


class StreetNameSpellingCorrectionTestCase(unittest.TestCase):
    def test_correct_street_name_spelling(self) -> None:
        test_cases = [
            ("Albantal", "St. Alban-Tal"),
            ("Albanvorstadt", "St. Alban-Vorstadt"),
            ("Johannsring", "St. Johanns-Ring"),
            ("Johannisring", "St. Johanns-Ring"),
            ("Nadelbgasse", "Nadelberg"),
            ("Pfrtergasse", "Pfirtergasse"),
            ("Riehenteichweg", "Riehenteichstrasse"),
            ("Spalenbgasse", "Spalenberg"),
            ("Spaleningasse", "Spalenberg"),
            ("St. Johanns-Ring", "St. Johanns-Ring"),
            ("Riehenteichweg", "Riehenteichstrasse"),
            ("Johannringweg", "St. Johanns-Rheinweg"),
            ("Thierst-Allee", "Thiersteinerallee"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = standardize_street_name(input_str)

                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
