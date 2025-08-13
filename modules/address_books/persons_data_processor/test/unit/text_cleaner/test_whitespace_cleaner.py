import unittest

from modules.address_books.persons_data_processor.src.text_cleaner.whitespace_cleaner import (
    WHITESPACE_PATTERNS_AND_REPL,
)
from modules.address_books.persons_data_processor.src.util.regex.apply_regex_patterns import (
    apply_regex_patterns,
)


class WhitespaceCleanerTestCase(unittest.TestCase):
    def test_clean_up_whitespace(self) -> None:
        test_cases = [
            ("   Peter Müller", "Peter Müller"),
            ("Peter Müller   ", "Peter Müller"),
            ("     Peter Müller   ", "Peter Müller"),
            ("   Peter  Müller   ", "Peter Müller"),
            ("Peter Müller", "Peter Müller"),
            (
                " Peter Müller    Peter Müller       Peter Müller Peter Müller",
                "Peter Müller Peter Müller Peter Müller Peter Müller",
            ),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = apply_regex_patterns(test_input, WHITESPACE_PATTERNS_AND_REPL)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
