import unittest

from modules.persons.src.cleaner.text_cleaner.parenthesis_handler import (
    clean_up_parenthesis,
)


class HandleParenthesisTestCase(unittest.TestCase):
    def test_clean_up_parenthesis(self):
        test_cases = [
            ("( Gottlieb", "Gottlieb"),
            ("Stockmeyer( Klausfelder Ludw.", "Stockmeyer Klausfelder Ludw."),
            ("Boller Müller( Vondann Anna", "Boller Müller Vondann Anna"),
            ("Boller Müller(", "Boller Müller"),
            (
                "Ob. Batteriew. ( Bur-au 2 Gerberg.)",
                "Ob. Batteriew. (Bur-au 2 Gerberg.)",
            ),
            ("Abom( Helene", "Abom Helene"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = clean_up_parenthesis(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\nActual: '{actual}'\nExpected: '{expected}'",
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
            ("G(ot(tli)eb", "G (ottli) eb"),
            ("( ()Go(((())ttlieb", "(Go) ttlieb"),
            ("Wyss (- Schumacher) Fritz", "Wyss (-Schumacher) Fritz"),
            ("Gottlieb (Müller)", "Gottlieb (Müller)"),
            ("Häusel((Kreis)Karl", "Häusel (Kreis) Karl"),
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

    def test_clean_up_whitespace_before_and_after_parenthesis(self):
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
                actual = clean_up_parenthesis(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch at case #{i + 1}:\n'{actual}' != '{expected}'"
                    f"\n\nFor input: '{input_str}'",
                )
