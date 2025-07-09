import unittest

from modules.persons.src.parser.text_sanitizer import (
    clean_text_lines,
    remove_unmatched_parenthesis,
    has_line_break,
    clean_up_parenthesis,
)


class TextSanitizerTestCase(unittest.TestCase):
    def test_clean_text_lines(self):
        test_cases = [
            ("Siegmann-| Höfer Trangott\n", "Siegmann-Höfer Trangott"),
            ("½ — Suppiger ", "-Suppiger"),
            ("fractext  f text  f -Vischer Theod.", "f-Vischer Theod."),
            ("Märklin fractext text — Jaecck Alfr.", "Märklin-Jaecck Alfr."),
        ]

        actual_output = clean_text_lines([tc[0] for tc in test_cases])

        for i, (actual, (_, expected)) in enumerate(zip(actual_output, test_cases)):
            with self.subTest(i=i, input=test_cases[i][0]):
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch at case #{i + 1}:\n'{actual}' != '{expected}'",
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
                actual = remove_unmatched_parenthesis(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch at case #{i + 1}:\n'{actual}' != '{expected}'",
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
                    f"\n\nMismatch at case #{i + 1}:\n'{actual_output[0]}' != '{expected}'",
                )

    def test_check_if_has_line_break(self):
        test_cases = [
            (("Struchen Emanuel, Schuhmacherstr., 93", "Elsässerstr."), True),
            (("Struchen Emanuel, Schuhmacherstr.,", "93 Elsässerstr."), True),
            (("Struchen Emanuel, Schuhmacher-", "str.,93 Elsässerstr."), True),
            (("", ""), False),
            (
                (
                    "Struchen E., Prokurist, 93 Elsässerstr.",
                    "Struchen E., Prokurist, 93 Elsässerstr.",
                ),
                False,
            ),
        ]

        for i, (input_lines, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_lines):
                actual_output = has_line_break(input_lines[0], input_lines[1])
                self.assertEqual(
                    actual_output,
                    expected,
                    f"\n\nMismatch at case #{i + 1}:\n'{actual_output}' != '{expected}'",
                )

    def test_clean_up_unmatched_parenthesis(self):
        test_cases = [
            ("( Gottlieb", "Gottlieb"),
            ("Gottli(eb", "Gottlieb"),
            ("Gottlieb ) ", "Gottlieb"),
            ("Got)tlieb", "Gottlieb"),
            ("()Gottlieb", "Gottlieb"),
            ("( )Gottlieb", "Gottlieb"),
            ("( )Gottlieb", "Gottlieb"),
            ("( ()Gottlieb", "Gottlieb"),
            ("G(ot(tli)eb", "G(ottli)eb"),
            ("( ()Go(((())ttlieb", "(Go)ttlieb"),
            ("Wyss (- Schumacher) Fritz", "Wyss (-Schumacher) Fritz"),
            ("Gottlieb (Müller)", "Gottlieb (Müller)"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = clean_up_parenthesis(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch at case #{i + 1}:\n'{actual}' != '{expected}'"
                    f"\n\nFor input: '{input_str}'",
                )
