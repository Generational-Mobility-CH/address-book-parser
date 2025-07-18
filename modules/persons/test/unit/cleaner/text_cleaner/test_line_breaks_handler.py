import unittest

from modules.persons.src.cleaner.text_cleaner.line_breaks_handler import (
    merge_line_break,
    has_line_break,
)


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
                first_line = test_input[0]
                second_line = test_input[1]

                if has_line_break(first_line, second_line):
                    actual_output = merge_line_break(first_line, second_line)
                else:
                    actual_output = tag_no_line_break

                self.assertEqual(
                    actual_output,
                    expected,
                    f"\n\nMismatch:\n'{actual_output}' != '{expected}'",
                )
