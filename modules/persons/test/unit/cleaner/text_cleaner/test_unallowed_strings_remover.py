import unittest

from modules.persons.src.cleaner.text_cleaner.unallowed_strings_remover import (
    UNALLOWED_STRINGS_PATTERNS_AND_REPLACEMENT,
)
from modules.persons.src.util.apply_regex_patterns import apply_regex_patterns


class UnallowedStringsRemoverTestCase(unittest.TestCase):
    def test_remove_unallowed_strings(self) -> None:
        test_cases = [
            (("123415 Müller öäüÇ :^[]|'"), ("123415 Müller öäüÇ ")),
            (("Siegmann-| Höfer Trangott\n"), ("Siegmann- Höfer Trangott")),
            (("½ — Suppiger "), (" — Suppiger ")),
            (("fractext  f text  f -Vischer Theod."), (" -Vischer Theod.")),
            (("Märklin fractext text — Jäcck Alfr."), ("Märklin — Jäcck Alfr.")),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_cases[i][0]):
                actual = apply_regex_patterns(
                    test_input, UNALLOWED_STRINGS_PATTERNS_AND_REPLACEMENT
                )

                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch:\n'{actual}' != '{expected}'",
                )
