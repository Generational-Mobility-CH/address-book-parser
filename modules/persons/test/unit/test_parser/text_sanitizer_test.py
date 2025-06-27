import unittest

from modules.persons.src.parser.text_sanitizer import (
    clean_text_lines,
    clean_up_parenthesis,
)


class TextSanitizerTestCase(unittest.TestCase):
    def test_clean_text_lines(self):
        test_cases = [
            ("Siegmann-| Höfer Trangott\n", "Siegmann- Höfer Trangott"),
            ("½ — Suppiger ", "— Suppiger"),
            ("fractext  f text  f -Vischer Theod.", "f -Vischer Theod."),
        ]

        actual_output = clean_text_lines([tc[0] for tc in test_cases])

        for i, (actual, (_, expected)) in enumerate(zip(actual_output, test_cases)):
            with self.subTest(i=i, input=test_cases[i][0]):
                self.assertEqual(
                    actual,
                    expected,
                    f"Mismatch at case #{i + 1}: '{actual}' != '{expected}'",
                )

    def test_clean_up_parenthesis(self):
        test_cases = [
            ("( Gottlieb", " Gottlieb"),
            ("Stockmeyer( Klausfelder Ludw.", "Stockmeyer Klausfelder Ludw."),
            ("Boller Müller( Vondann Anna", "Boller Müller Vondann Anna"),
            ("Boller Müller(", "Boller Müller"),
            (
                "Ob. Batteriew. ( Bur-au 2 Gerberg.)",
                "Ob. Batteriew. ( Bur-au 2 Gerberg.)",
            ),
            ("Abom( Helene", "Abom Helene"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = clean_up_parenthesis(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"Mismatch at case #{i + 1}: '{actual}' != '{expected}'",
                )

    def test_line_breaks_merging(self):
        test_cases = [
            (
                ["Struchen Emanuel, Schuhmacherstr., 93", "Elsässerstr."],
                "Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.",
            ),
            (
                ["Struchen Emanuel, Schuhmacherstr., 93 El-", "sässerstr."],
                "Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.",
            ),
        ]

        for i, (input_lines, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_lines):
                actual_output = clean_text_lines(input_lines)
                self.assertEqual(
                    actual_output[0],
                    expected,
                    f"Mismatch at case #{i + 1}: '{actual_output[0]}' != '{expected}'",
                )
