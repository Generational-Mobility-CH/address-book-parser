import unittest

from modules.address_books.parser.src.cleaner.text_cleaner.dashes_cleaner import (
    DASHES_PATTERNS_AND_REPL,
)
from modules.address_books.parser.src.util.regex.apply_regex_patterns import (
    apply_regex_patterns,
)


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
                actual = apply_regex_patterns(test_input, DASHES_PATTERNS_AND_REPL)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
