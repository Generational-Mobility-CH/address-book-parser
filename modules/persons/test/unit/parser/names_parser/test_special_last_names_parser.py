import unittest

from modules.persons.src.parser.names_parser.special_last_names_parser import (
    merge_last_names_with_prefixes,
)


class SpecialLasNamesParserTest(unittest.TestCase):
    def test_handle_last_names_with_prefixes(self) -> None:
        test_cases = [
            ("Abt von der Bach Fritz", "Abt VonDerBach Fritz"),
            ("Abt von Der Bach Fritz", "Abt VonDerBach Fritz"),
            ("Abt-Van Der Bach Fritz", "Abt-VanDerBach Fritz"),
            ("Abt De la Bach Fritz", "Abt DeLaBach Fritz"),
            ("von Bach Fritz", "VonBach Fritz"),
            ("La Roche Müller Fritz", "LaRoche Müller Fritz"),
            ("La Roche-Müller Fritz", "LaRoche-Müller Fritz"),
            ("La Müller Fritz", "LaMüller Fritz"),
            ("Müller La Roche Fritz", "Müller LaRoche Fritz"),
            ("De la Roche Fritz", "DeLaRoche Fritz"),
            ("Von Karol", "VonKarol"),
            ("Karol Von Abc", "Karol VonAbc"),
            ("Leemann Le Grand Adolf", "Leemann LeGrand Adolf"),
            ("Leemann Müller Le Grand Adolf", "Leemann Müller LeGrand Adolf"),
            ("Le Christ Josef", "LeChrist Josef"),
            ("Bettoli De Zorzi Giov. Magazkn.", "Bettoli DeZorzi Giov. Magazkn."),
            ("Grimm Van der Mälen Heinr.", "Grimm VanDerMälen Heinr."),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                input_str = merge_last_names_with_prefixes(input_str)

                actual = input_str
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_handle_special_last_names_and_dash(self) -> None:
        test_cases = [
            ("-Van der Mälen Heinr.", "-VanDerMälen Heinr."),
            ("- Van der Mälen Heinr.", "- VanDerMälen Heinr."),
            ("de paris-Mälen Heinr.", "Deparis-Mälen Heinr."),
            ("Müller-Van der mälen Heinr.", "Müller-VanDermälen Heinr."),
            ("Müller-de Mälen Heinr.", "Müller-DeMälen Heinr."),
            ("de Mälen-Müller Heinr.", "DeMälen-Müller Heinr."),
            ("De la Roche-Mälen Heinr.", "DeLaRoche-Mälen Heinr."),
            ("Mälen-De la Roche Heinr.", "Mälen-DeLaRoche Heinr."),
            ("la Roche-Mälen Heinr.", "LaRoche-Mälen Heinr."),
            (
                "la Roche-Mälen Von der Schmitt Heinr.",
                "LaRoche-Mälen VonDerSchmitt Heinr.",
            ),
            (
                "Werthemann Von Werther-Von Cichomska Baronin Isabella",
                "Werthemann VonWerther-VonCichomska Baronin Isabella",
            ),
            (
                "Werthemann Von Werther-de la Roche Cichomska Baronin Isabella",
                "Werthemann VonWerther-DeLaRoche Cichomska Baronin Isabella",
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = merge_last_names_with_prefixes(input_str)

                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch for '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_names_with_overlapping_prefixes_stay_the_same(self):
        test_cases = [
            ("Depardieu Cecile", "Depardieu Cecile"),
            ("Aberle Abelde", "Aberle Abelde"),
            ("Aberle Haas Wwe. A. Doroth.", "Aberle Haas Wwe. A. Doroth."),
            ("Zumstein Aberle Carole", "Zumstein Aberle Carole"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = merge_last_names_with_prefixes(input_str)

                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch for '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
