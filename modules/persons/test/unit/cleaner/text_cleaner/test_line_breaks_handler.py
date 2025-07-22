import unittest

from modules.persons.src.cleaner.text_cleaner.line_breaks_handler import (
    merge_line_break,
    has_line_break,
)
from modules.persons.src.cleaner.text_cleaner.text_cleaner import clean_text


class HandleLineBreaksTestCase(unittest.TestCase):
    def test_line_breaks_merging(self) -> None:
        tag_no_line_break = "<NO LINE BREAK FOUND>"

        test_cases = [
            (
                ["Struchen-Müller Emanuel, Schuhmacher, 93", "Elsässerstr."],
                "Struchen-Müller Emanuel, Schuhmacher, 93 Elsässerstr.",
            ),
            (
                ["Struchen-Müller Emanuel, Schuhmacher, 93 El-", "sässerstr."],
                "Struchen-Müller Emanuel, Schuhmacher, 93 Elsässerstr.",
            ),
            (
                ["Struchen-Müller Emanuel, Schuhmacher, 93 Elsässerstr.", "abc"],
                tag_no_line_break,
            ),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_input):
                previous_line = test_input[0]
                current_line = test_input[1]

                if has_line_break(current_line, previous_line):
                    actual_output = merge_line_break(current_line, previous_line)
                else:
                    actual_output = tag_no_line_break

                self.assertEqual(
                    actual_output,
                    expected,
                    f"\n\nMismatch:\n'{actual_output}' != '{expected}'",
                )

    def test_line_breaks_within_cleaner(self) -> None:
        test_cases = [
            (
                ["Struchen-Müller Emanuel, Schuhmacher, 93", "Elsässerstr."],
                ["Struchen-Müller Emanuel, Schuhmacher, 93 Elsässerstr."],
            ),
            (
                ["Struchen-Müller Emanuel, Schuhmacher, 93 El-", "sässerstr."],
                ["Struchen-Müller Emanuel, Schuhmacher, 93 Elsässerstr."],
            ),
            (
                ["Struchen-Müller Emanuel, Schuhmacher, 93 Elsässerstr.", "abc"],
                ["Struchen-Müller Emanuel, Schuhmacher, 93 Elsässerstr.", "abc"],
            ),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_input):
                actual = clean_text(test_input)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
