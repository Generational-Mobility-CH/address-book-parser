import unittest

from modules.persons.src.cleaner.text_cleaner.dashes_handler import (
    DASHES_PATTERNS_AND_REPLACEMENT,
)
from modules.persons.src.util.apply_regex_patterns import apply_regex_patterns


class DasherHandlerTestCase(unittest.TestCase):
    def test_dashes_conversion(self) -> None:
        test_cases = [
            ("Siegmann-Höfer Trangott", "Siegmann-Höfer Trangott"),
            ("— Suppiger", "-Suppiger"),
            ("—————— Suppiger", "-Suppiger"),
            ("—————— Suppiger---- ", "-Suppiger-"),
            ("—————— Suppiger---- Müller", "-Suppiger-Müller"),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = apply_regex_patterns(
                    test_input, DASHES_PATTERNS_AND_REPLACEMENT
                )

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
