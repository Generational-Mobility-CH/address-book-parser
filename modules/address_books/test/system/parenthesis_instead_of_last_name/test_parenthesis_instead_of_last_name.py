import unittest
from pathlib import Path

from modules.shared.repository.supported_file_types import (
    SupportedFileTypes,
)
from modules.address_books.src.__main__ import main
from system.util.assert_csv_files_are_equal import assert_csv_files_are_equal


class ParenthesisInsteadOfLastNameTestCase(unittest.TestCase):
    def test_parenthesis_instead_of_last_name(self) -> None:
        test_dir = Path("system") / "parenthesis_instead_of_last_name"
        test_input = test_dir / "fixtures"
        expected = test_input / "expected.csv"
        actual = test_dir / "expected.csv"
        column_names = ["original_names"]

        main(test_input, actual, SupportedFileTypes.CSV, column_names)

        assert_csv_files_are_equal(expected, actual)
