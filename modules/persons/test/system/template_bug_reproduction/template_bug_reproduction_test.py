import unittest

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.__main__ import main
from system.util.assert_csv_files_are_equal import assert_csv_files_are_equal


class TemplateBugReproductionTestCase(unittest.TestCase):
    def test_bug(self):
        test_dir = "system/template_bug_reproduction"
        test_input = f"{test_dir}/fixtures"
        expected = f"{test_dir}/fixtures/expected.csv"
        actual = f"{test_dir}/actual.csv"
        relevant_columns = [
            "original_names",
            "last_names",
            "first_names",
            # "job",
            # "address",
            # "year",
            # "pdf_page_number",
        ]

        main(test_input, actual, SupportedFileTypes.CSV, relevant_columns)

        assert_csv_files_are_equal(expected, actual)
