import unittest
from pathlib import Path

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.__main__ import main
from system.util.assert_csv_files_are_equal import assert_csv_files_are_equal


class TemplateBugReproductionTestCase(unittest.TestCase):
    def test_when_no_give_column_names_then_all_attribute_names_are_deduced(
        self,
    ) -> None:
        test_dir = Path("unit/csv/book_to_csv")
        test_input = test_dir / "fixtures"
        expected = test_input / "expected.csv"
        actual = test_dir / "actual.csv"

        main(test_input, actual, SupportedFileTypes.CSV)

        assert_csv_files_are_equal(expected, actual)
