import unittest

from modules.persons.src.parser.names.special_last_names_parser import (
    handle_special_last_names,
    find_special_last_name_keyword,
)


class MyTestCase(unittest.TestCase):
    def test_handle_special_last_names_if_present(self):
        test_cases = [
            # ("Abt von der Bach Fritz", "Abt VonDerBach Fritz"),
            # ("Abt von Der Bach Fritz", "Abt VonDerBach Fritz"),
            # ("Abt Van Der Bach Fritz", "Abt VanDerBach Fritz"),
            # ("Abt De la Bach Fritz", "Abt DeLaBach Fritz"),
            ("von Bach Fritz", "VonBach Fritz"),
            ("La Roche Müller Fritz", "LaRoche Müller Fritz"),
            ("De la Roche Fritz", "DeLaRoche Fritz"),
            ("Von Karol", "VonKarol"),
            ("Karol Von Abc", "Karol VonAbc"),
            ("Leemann Le Grand Adolf", "Leemann LeGrand Adolf"),
            ("Leemann Müller Le Grand Adolf", "Leemann Müller LeGrand Adolf"),
            ("Le Christ Josef", "LeChrist Josef"),
            # This cases should remain unchanged
            ("Aberle Haas Wwe. A. Doroth.", "Aberle Haas Wwe. A. Doroth."),
            ("Zumstein Aberle Carole", "Zumstein Aberle Carole"),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                if k := find_special_last_name_keyword(input_str):
                    input_str = handle_special_last_names(input_str, k)

                actual = input_str
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch in `first_names` at case #{i + 1}:\nInput: '{input_str}'\nExpected: '{expected}'\nActual:   '{actual}'",
                )
