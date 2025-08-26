import unittest
from pathlib import Path

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons_data_processor.src.__main__ import main
from system.util.assert_csv_files_are_equal import assert_csv_files_are_equal


class HallucinationsCheckTestCase(unittest.TestCase):
    def test_when_same_person_repeated_on_same_page_then_ignore_person(self) -> None:
        test_dir = Path("system") / "repeated_persons_are_added_only_once"
        test_input = test_dir / "fixtures"
        expected = test_input / "expected.csv"
        actual = test_dir / "expected.csv"
        relevant_columns = [
            "original_names",
            "job",
            "address__street_name",
            "address__house_number",
            "pdf_page_number",
        ]

        main(test_input, actual, SupportedFileTypes.CSV, relevant_columns)

        assert_csv_files_are_equal(expected, actual)
