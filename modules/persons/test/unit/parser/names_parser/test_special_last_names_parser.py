import unittest

from modules.persons.src.parser.names_parser.special_last_names_parser import (
    handle_multi_part_last_names,
    find_multi_part_last_names_keyword,
)


class SpecialLasNamesParserTest(unittest.TestCase):
    def test_handle_special_last_names_if_present(self) -> None:
        test_cases = [
            ("Abt von der Bach Fritz", "Abt VonDerBach Fritz"),
            ("Abt von Der Bach Fritz", "Abt VonDerBach Fritz"),
            ("Abt Van Der Bach Fritz", "Abt VanDerBach Fritz"),
            ("Abt De la Bach Fritz", "Abt DeLaBach Fritz"),
            ("von Bach Fritz", "VonBach Fritz"),
            ("La Roche Müller Fritz", "LaRoche Müller Fritz"),
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
            # This cases should remain unchanged
            ("Aberle Haas Wwe. A. Doroth.", "Aberle Haas Wwe. A. Doroth."),
            ("Zumstein Aberle Carole", "Zumstein Aberle Carole"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                if k := find_multi_part_last_names_keyword(input_str):
                    input_str = handle_multi_part_last_names(input_str, k)

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
            ("de paris-Mälen Heinr.", "DeParis-Mälen Heinr."),
            ("Müller-Van der Mälen Heinr.", "Müller-VanDerMälen Heinr."),
            ("Müller-de Mälen Heinr.", "Müller-DeMälen Heinr."),
            ("de Mälen-Müller Heinr.", "DeMälen-Müller Heinr."),
            ("De la Roche-Mälen Heinr.", "DeLaRoche-Mälen Heinr."),
            ("Mälen-De la Roche Heinr.", "Mälen-DeLaRoche Heinr."),
            ("la Roche-Mälen Heinr.", "LaRoche-Mälen Heinr."),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                if k := find_multi_part_last_names_keyword(input_str):
                    actual = handle_multi_part_last_names(input_str, k)

                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
