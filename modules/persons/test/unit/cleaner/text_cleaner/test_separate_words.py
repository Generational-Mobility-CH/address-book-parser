import unittest

from modules.persons.src.cleaner.text_cleaner.words_separator import separate_words


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

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = separate_words(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_ensure_space_after_dot(self) -> None:
        test_cases = [
            ("Müller J.Ls.", "Müller J. Ls."),
            ("Müller Rob.Saml.", "Müller Rob. Saml."),
            ("MüllerRob.Saml.", "Müller Rob. Saml."),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = separate_words(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
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

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = separate_words(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'"
                    f"\n\nFor input: '{input_str}'",
                )
