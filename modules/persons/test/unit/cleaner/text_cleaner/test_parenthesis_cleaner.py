import unittest

from modules.persons.src.cleaner.text_cleaner.parenthesis_cleaner import (
    PARENTHESIS_PATTERNS_AND_REPL,
    remove_unmatched_parenthesis,
)
from modules.persons.src.util.apply_regex_patterns import apply_regex_patterns


class HandleParenthesisTestCase(unittest.TestCase):
    def test_clean_up_parenthesis(self) -> None:
        test_cases = [
            ("( Gottlieb )", "(Gottlieb)"),
            (
                "Gottlieb     (         Gottlieb )Gottlieb",
                "Gottlieb     (Gottlieb)Gottlieb",
            ),
            (
                "Ob. Batteriew. ( Bur-au 2 Gerberg.)",
                "Ob. Batteriew. (Bur-au 2 Gerberg.)",
            ),
            (
                "Ob. Batteriew. ( Bur-au 2 Gerberg. )",
                "Ob. Batteriew. (Bur-au 2 Gerberg.)",
            ),
            (
                "Ob. Batteriew. (Bur-au 2 Gerberg. )",
                "Ob. Batteriew. (Bur-au 2 Gerberg.)",
            ),
            (
                "Ob. Batteriew. ((Bur-au 2 Gerberg. )",
                "Ob. Batteriew. ((Bur-au 2 Gerberg.)",
            ),
            ("()Gottlieb", "Gottlieb"),
            ("(   )Gottlieb", "Gottlieb"),
            ("Gottl( )ieb", "Gottlieb"),
            ("Wyss (- Schumacher) Fritz", "Wyss (-Schumacher) Fritz"),
            ("(Wyss -) Schumacher Fritz", "(Wyss-) Schumacher Fritz"),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = apply_regex_patterns(test_input, PARENTHESIS_PATTERNS_AND_REPL)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )

    def test_clean_up_unmatched_parenthesis(self) -> None:
        test_cases = [
            ("( (Gottlieb", " Gottlieb"),
            ("Gottli(eb", "Gottlieb"),
            ("Gottlieb ) ", "Gottlieb  "),
            ("Got)tlieb", "Gottlieb"),
            ("( ()Gottlieb", "( )Gottlieb"),
            ("G(ot(tli)eb", "G(ottli)eb"),
            ("( ()Go(((())ttlieb", "( ()Go())ttlieb"),
            ("Gottlieb (Müller)", "Gottlieb (Müller)"),
            ("Häusel((Kreis)Karl", "Häusel(Kreis)Karl"),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = remove_unmatched_parenthesis(test_input)

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
