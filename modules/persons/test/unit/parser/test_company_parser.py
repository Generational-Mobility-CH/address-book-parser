import unittest
from pathlib import Path

from modules.persons.src.models.person.person_data_parts import PersonDataParts
from modules.persons.src.parser.company_parser import is_company


class RemoveCompaniesTestCase(unittest.TestCase):
    def test_remove_companies(self) -> None:
        test_file = Path("unit/parser/fixtures/remove_companies_test_input.txt")

        expected_remaining_lines = [
            "— -Neukomm Emil, Kfm., 44 Elisabethenstr. (Frau: Damenschneiderin.)\n",
            "— -Ritter Ad., Buchh., 47 Delsbergerallee.\n",
        ]

        with open(test_file, "r") as f:
            all_lines = f.readlines()

        for i, line in enumerate(all_lines):
            with self.subTest(i=i, line=line.strip()):
                information = PersonDataParts.from_list(line.split(","))
                is_company_line = is_company(information)

                if line in expected_remaining_lines:
                    self.assertFalse(
                        is_company_line,
                        f"Line should NOT be removed, but was detected as company:\n{line}",
                    )
                else:
                    self.assertTrue(
                        is_company_line,
                        f"Line should be removed, but was not detected as company:\n{line}",
                    )

    def test_is_company(self) -> None:
        test_cases = [
            (PersonDataParts("Hotel Metropole-Monopole A.-G.", ""), True),
            (PersonDataParts("Gautschy-Kuhn A.-G.", ""), True),
            (PersonDataParts("Müller-Abt Heinrich", "10 Bahnhofstr."), False),
        ]

        for i, (test_input, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=test_input):
                actual = is_company(test_input)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch:\nInput: '{test_input}'\nExpected: '{expected}'\nActual: '{actual}'",
                )
