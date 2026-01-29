import unittest
from pathlib import Path

from modules.__main__ import main
from modules.repository.src.supported_file_types import (
    SupportedFileTypes,
)
from system.fixtures.fixtures_dir_path import FIXTURES_DIR
from modules.shared.utility.assert_csv_files_are_equal import assert_csv_files_are_equal


class TemplateBugReproductionTestCase(unittest.TestCase):
    def test_bug(self) -> None:
        test_resources = FIXTURES_DIR / Path(__file__).name.removeprefix(
            "test_"
        ).removesuffix(".py")
        test_input = test_resources / "test_input"
        expected = test_resources / "expected.csv"
        actual = test_resources / "actual.csv"

        relevant_columns = [
            "original_entry",
            "address__street_name",
            "address__house_number",
        ]

        main(test_input, actual, SupportedFileTypes.CSV, relevant_columns)

        assert_csv_files_are_equal(expected, actual)
