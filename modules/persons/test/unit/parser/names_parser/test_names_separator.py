import unittest

from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.names_parser.names_separator import separate_names


class HandleGeschiedenTest(unittest.TestCase):
    def test_handle_geschieden(self):
        test_cases = [
            (
                "Egg Eggemann gesch. Bödecker Emma",
                PersonNames("Emma", "Egg Eggemann Gesch. Bödecker"),
            ),
            ("Abrv Abt gesch. Abt Frida", PersonNames("Frida", "Abrv Abt Gesch. Abt")),
            (
                "Braun (gesch. Maerklin) Marie Elis.",
                PersonNames("Marie Elis.", "Braun (Gesch. Maerklin)"),
            ),
            (
                "Winkler (gesch. Hurter) Maria Kath.",
                PersonNames("Maria Kath.", "Winkler (Gesch. Hurter)"),
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = separate_names(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_merged_names_by_dot(self):
        test_cases = [
            (
                "J.Ls.",
                PersonNames("Ls.", "J."),
            ),
            (
                "Rob.Saml.",
                PersonNames("Saml.", "Rob."),
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = separate_names(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
