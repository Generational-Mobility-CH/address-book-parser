import unittest

from modules.persons.src.cleaner.text_cleaner.text_cleaner import clean_text_lines


class HandleLineBreaksTestCase(unittest.TestCase):
    def test_line_breaks_merging(self) -> None:
        test_cases = [
            (
                ["Struchen Emanuel, Schuhmacherstr., 93", "Elsässerstr."],
                "Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.",
            ),
            (
                ["Struchen Emanuel, Schuhmacherstr., 93 El-", "sässerstr."],
                "Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.",
            ),
            (
                ["Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.", "abc"],
                "Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.",
            ),
        ]

        for i, (input_lines, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_lines):
                actual_output = clean_text_lines(input_lines)
                self.assertEqual(
                    actual_output[0],
                    expected,
                    f"\n\nMismatch:\n'{actual_output[0]}' != '{expected}'",
                )
