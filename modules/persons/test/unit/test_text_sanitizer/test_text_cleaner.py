import unittest

from modules.persons.src.parser.text_sanitizer import (
    clean_text_lines,
    remove_if_contains_unallowed_word,
    clean_up_parenthesis,
)


class TextSanitizerTestCase(unittest.TestCase):
    def test_clean_text_lines(self):
        test_input = [
            "Siegmann-| Höfer Trangott\n",
            "½ — Suppiger ",
            "fractext  f text  f -Vischer Theod.",
        ]

        expected_output = [
            "Siegmann- Höfer Trangott",
            "— Suppiger",
            "f -Vischer Theod.",
        ]

        actual_output = clean_text_lines(test_input)

        for i, (actual, expected) in enumerate(zip(actual_output, expected_output)):
            self.assertEqual(
                actual,
                expected,
                f"Mismatch at list element nr. {i + 1}: '{actual}' != '{expected}'",
            )

    def test_remove_if_contains_unallowed_word(self):
        test_input = [
            "Freiermuth fracmathfrakHmathfrakH - König Arn.",
            "Fehlmann fracmathfrakzmathfrakz -Francke Walt.Dr.D.S.",
            "Mundschin( fracmathbffmathbff— Marguerite",
            "Muhmenthaler fracmathbffmathbff— Jak.",
        ]

        expected_output = [
            "Freiermuth - König Arn.",
            "Fehlmann -Francke Walt.Dr.D.S.",
            "Mundschin( Marguerite",
            "Muhmenthaler Jak.",
        ]

        actual_output = [remove_if_contains_unallowed_word(s) for s in test_input]

        for i, (actual, expected) in enumerate(zip(actual_output, expected_output)):
            self.assertEqual(
                actual,
                expected,
                f"Mismatch at list element nr. {i + 1}: '{actual}' != '{expected}'",
            )

    def test_clean_up_parenthesis(self):
        test_input = [
            "( Gottlieb",
            "Stockmeyer( Klausfelder Ludw.",
            "Boller Müller( Vondann Anna",
            "Boller Müller(",
            "Ob. Batteriew. ( Bur-au 2 Gerberg.)",
            "Abom( Helene",
        ]

        expected_output = [
            " Gottlieb",
            "Stockmeyer Klausfelder Ludw.",
            "Boller Müller Vondann Anna",
            "Boller Müller",
            "Ob. Batteriew. ( Bur-au 2 Gerberg.)",
            "Abom Helene",
        ]

        actual_output = [clean_up_parenthesis(s) for s in test_input]

        for i, (actual, expected) in enumerate(zip(actual_output, expected_output)):
            self.assertEqual(
                actual,
                expected,
                f"Mismatch at list element nr. {i + 1}: '{actual}' != '{expected}'",
            )

    def test_line_breaks_merging(self):
        test_input = [
            "Struchen Emanuel, Schuhmacherstr., 93",
            "Elsässerstr.",
            "Struchen Emanuel, Schuhmacherstr., 93 El-",
            "sässerstr.",
        ]

        expected_output = [
            "Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.",
            "Struchen Emanuel, Schuhmacherstr., 93 Elsässerstr.",
        ]

        actual_output = clean_text_lines(test_input)

        for i, (actual, expected) in enumerate(zip(actual_output, expected_output)):
            self.assertEqual(
                actual,
                expected,
                f"\n\nMismatch at list element nr. {i + 1}: '{actual}' != '{expected}'",
            )
