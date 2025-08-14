import unittest

from modules.address_books.persons_data_processor.src.text_cleaner.words_separator import (
    SEPARATE_WORDS_PATTERNS_AND_REPL,
)
from modules.address_books.persons_data_processor.src.utility.regex.apply_regex_patterns import (
    apply_regex_patterns,
)


class UnmergeWordsTestCase(unittest.TestCase):
    def test_unmerge_camel_cased_names(self) -> None:
        test_cases = [
            ("MüllerJohann", "Müller Johann"),
            ("MüllerRobbinsSaml", "Müller Robbins Saml"),
            ("ConusAlfr.", "Conus Alfr."),
            ("Bolinger-GrossSamI.", "Bolinger-Gross Sam I."),
            ("Bolley-BerkesK.", "Bolley-Berkes K."),
            ("Brom-HoffstetterJoh.", "Brom-Hoffstetter Joh."),
            ("BurgerAlb. Rosina", "Burger Alb. Rosina"),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_input):
                actual = apply_regex_patterns(
                    test_input, SEPARATE_WORDS_PATTERNS_AND_REPL
                )

                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{test_input}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_ensure_space_after_dot(self) -> None:
        test_cases = [
            ("Müller J.Ls.", "Müller J. Ls."),
            ("Müller Rob.Saml.", "Müller Rob. Saml."),
            ("MüllerRob.Saml.", "Müller Rob. Saml."),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_input):
                actual = apply_regex_patterns(
                    test_input, SEPARATE_WORDS_PATTERNS_AND_REPL
                )

                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{test_input}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_ensure_space_before_and_after_parenthesis(self) -> None:
        test_cases = [
            ("Gottlieb(Müller)", "Gottlieb (Müller)"),
            ("(Müller) Gottlieb", "(Müller) Gottlieb"),
            ("(Müller)Gottlieb", "(Müller) Gottlieb"),
            ("Häusel(Kreis)Karl", "Häusel (Kreis) Karl"),
            ("Häusel-(Kreis)Karl", "Häusel- (Kreis) Karl"),
            ("Häusel (Kreis) Karl", "Häusel (Kreis) Karl"),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_input):
                actual = apply_regex_patterns(
                    test_input, SEPARATE_WORDS_PATTERNS_AND_REPL
                )

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'"
                    f"\n\nFor input: '{test_input}'",
                )
