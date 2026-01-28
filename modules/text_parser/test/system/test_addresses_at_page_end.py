import unittest
from pathlib import Path

from modules.__main__ import main
from modules.repository.src.supported_file_types import (
    SupportedFileTypes,
)
from system.fixtures.fixtures_dir_path import FIXTURES_DIR
from system.util.assert_csv_files_are_equal import assert_csv_files_are_equal


class AddressAtEnfOfPageTestCase(unittest.TestCase):
    def test_if_address_is_at_page_end_then_first_line_of_next_page_is_not_in_address(
        self,
    ) -> None:
        test_resources = FIXTURES_DIR / Path(__file__).name.removeprefix(
            "test_"
        ).removesuffix(".py")
        test_input = test_resources / "test_input"
        expected = test_resources / "expected.csv"
        actual = test_resources / "actual.csv"

        relevant_columns = [
            "first_names",
            "last_names",
            "partner_last_names",
            "address__street_name",
            "address__house_number",
            "original_entry",
        ]

        main(test_input, actual, SupportedFileTypes.CSV, relevant_columns)

        assert_csv_files_are_equal(expected, actual)
