import csv
import os
import unittest

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.__main__ import main


class ParenthesisBugTestCase(unittest.TestCase):
    def test_parenthesis_instead_of_last_name_bug(self):
        test_input = "../test/system/tc_parenthesis_instead_of_last_name_bug/fixtures"
        test_output = "system/tc_parenthesis_instead_of_last_name_bug/test_output.csv"
        expected_file = "system/tc_parenthesis_instead_of_last_name_bug/fixtures/expected_test_output.csv"

        main(test_input, test_output, SupportedFileTypes.CSV)

        with (
            open(expected_file, newline="") as expected,
            open(test_output, newline="") as actual,
        ):
            reader = csv.DictReader(actual)
            actual_lines = set(
                tuple(
                    (k, v.strip())
                    for k, v in row.items()
                    if k != "person_id" and k != "year" and k != "pdf_page_number"
                )
                for row in reader
            )

            reader = csv.DictReader(expected)
            expected_lines = set(
                tuple((k, v.strip()) for k, v in row.items()) for row in reader
            )

            if expected_lines != actual_lines:
                missing_lines = expected_lines - actual_lines
                superfluous_lines = actual_lines - expected_lines
                if missing_lines:
                    print(f"\nMissing lines:\n{missing_lines}")
                if superfluous_lines:
                    print(f"\nSuperfluous lines:\n{superfluous_lines}")
                self.fail("CSV files differ")
            else:
                os.remove(test_output)


if __name__ == "__main__":
    unittest.main()
