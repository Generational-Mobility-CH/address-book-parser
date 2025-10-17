import unittest
from pathlib import Path

from modules.address_books.src.__main__ import main
from modules.shared.repository.supported_file_types import (
    SupportedFileTypes,
)
from system.util.assert_csv_files_are_equal import assert_csv_files_are_equal


class TemplateBugReproductionTestCase(unittest.TestCase):
    def test_if_address_is_at_page_end_then_first_line_of_next_page_is_not_in_address(
        self,
    ) -> None:
        test_dir = Path("system") / "addresses_at_page_end_are_parsed_correctly"
        test_input = test_dir / "fixtures"
        expected = test_input / "expected.csv"
        actual = test_dir / "expected.csv"
        relevant_columns = [
            "address__street_name",
            "address__house_number",
            "original_names",
        ]

        main(test_input, actual, SupportedFileTypes.CSV, relevant_columns)

        assert_csv_files_are_equal(expected, actual)
