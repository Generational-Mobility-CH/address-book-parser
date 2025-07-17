import unittest

from modules.persons.src.models.person.person_names import PersonNames
from modules.persons.src.parser.names_parser.names_parser import parse_names


class NamesSeparatorTest(unittest.TestCase):
    def test_handle_divorced(self) -> None:
        test_cases = [
            (
                "Egg Eggemann gesch. Bödecker Emma",
                PersonNames("Emma", "Egg EggemannGesch.Bödecker"),
            ),
            ("Abrv AbtGesch.Abt Frida", PersonNames("Frida", "Abrv AbtGesch.Abt")),
            (
                "Braun (gesch. Maerklin) Marie Elis.",
                PersonNames(
                    "Elis.", "Braun(Gesch.Maerklin) Marie"
                ),  # because len(name_parts) == 3
            ),
            (
                "Winkler (gesch. Hurter) Maria Kath.",
                PersonNames(
                    "Kath.", "Winkler(Gesch.Hurter) Maria"
                ),  # because len(name_parts) == 3
            ),
            (
                "wiederkehr (gesch. plattner) a. m.",
                PersonNames("A. M.", "Wiederkehr(Gesch.Plattner)"),
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

    def test_handle_names_with_more_than_four_parts(self) -> None:
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

    def test_merged_names_by_dot(self) -> None:
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

    def test_names_with_auch(self) -> None:
        test_cases = [
            (
                "Komarek (auch Kohn) -Hernbal Abram",
                PersonNames("Abram", "Komarek(AuchKohn)-Hernbal"),
            ),
            (
                "Komarek (auch Kohn) Regina",
                PersonNames("Regina", "Komarek(AuchKohn)"),
            ),
            (
                "Eschbach (auch Aeschbach) -Dürenberger Ed.",  # Name should be splited at "Ed."
                PersonNames("Ed.", "Eschbach(Auchaeschbach)-Dürenberger"),
            ),
            (
                "Höckle (auch Höglin) -Girov Wwe. Anna",  # Name should be splited at "Wwe."
                PersonNames("Wwe. Anna", "Höckle(Auchhöglin)-Girov"),
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
