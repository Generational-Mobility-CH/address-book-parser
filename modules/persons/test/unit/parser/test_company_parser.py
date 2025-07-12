import unittest

from modules.persons.src.models.person.person_data_parts import PersonDataParts
from modules.persons.src.parser.company_parser import is_company


class RemoveCompaniesTestCase(unittest.TestCase):
    def test_remove_companies(self):
        test_file = "unit/parser/fixtures/remove_companies_test_input.txt"

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
