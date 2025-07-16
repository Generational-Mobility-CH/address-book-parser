import unittest

from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.names_parser.names_parser import parse_names


class NamesSeparatorTest(unittest.TestCase):
    def test_handle_divorced(self):
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
            (
                "wiederkehr (gesch. plattner) a. m.",
                PersonNames("A. M.", "Wiederkehr (Gesch. Plattner)"),
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = parse_names(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_unmerge_names_without_space_after_dot(self):
        test_cases = [
            (
                "Müller J.Ls.",
                PersonNames("J. Ls.", "Müller"),
            ),
            (
                "Müller Rob.Saml.",
                PersonNames("Rob. Saml.", "Müller"),
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = parse_names(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_unmerge_camel_cased_names(self):
        test_cases = [
            (
                "MüllerJohann",
                PersonNames("Johann", "Müller"),
            ),
            (
                "MüllerRobbinsSaml",
                PersonNames("Saml", "Müller Robbins"),
            ),
            (
                "ConusAlfr.",
                PersonNames("Alfr.", "Conus"),
            ),
            (
                "Bolinger-GrossSamI.",
                PersonNames("I.", "Bolinger-Gross Sam"),
            ),
            (
                "Bolley-BerkesK.",
                PersonNames("K.", "Bolley-Berkes"),
            ),
            (
                "Brom-HoffstetterJoh.",
                PersonNames("Joh.", "Brom-Hoffstetter"),
            ),
            (
                "BurgerAlb. Rosina",
                PersonNames("Alb. Rosina", "Burger"),
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = parse_names(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )

    def test_handle_names_with_more_than_four_parts(self):
        test_cases = [
            (
                "Amans Madeux J. J. C.",
                PersonNames("J. J. C.", "Amans Madeux"),
            ),
            ("Bieler Fross Joh. Fr. B.", PersonNames("Joh. Fr. B.", "Bieler Fross")),
            (
                "Wirth (-Brunner) Pfarrer Joh. Zwingli",
                PersonNames("Joh. Zwingli", "Wirth (-Brunner) Pfarrer"),
            ),
            (
                "Bender Bélat (-Studer) Fr. Et.",
                PersonNames("Fr. Et.", "Bender Bélat (-Studer)"),
            ),
            (
                "Häusel Kunz Wwe. Maria",
                PersonNames("Wwe. Maria", "Häusel Kunz"),
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = parse_names(input_str)
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
                actual = parse_names(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{input_str}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
