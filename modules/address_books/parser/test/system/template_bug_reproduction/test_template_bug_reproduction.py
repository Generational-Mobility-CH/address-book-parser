import unittest
from pathlib import Path

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.address_books.parser.src.__main__ import main
from system.util.assert_csv_files_are_equal import assert_csv_files_are_equal


class TemplateBugReproductionTestCase(unittest.TestCase):
    def test_bug(self) -> None:
        test_dir = (
            Path("system") / "template_bug_reproduction"
        )  # rename path end according to test directory
        test_input = test_dir / "fixtures"
        expected = test_input / "expected.csv"
        actual = test_dir / "actual.csv"
        relevant_columns = [
            "original_names",
            # "job",
            # "year",
            # "pdf_page_number",
            # "address__street_name",
            # "address__house_number",
        ]

        main(test_input, actual, SupportedFileTypes.CSV, relevant_columns)

        assert_csv_files_are_equal(expected, actual)
