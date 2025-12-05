import unittest
from pathlib import Path

from libs.file_handler.src.util.get_year_from_file_name import get_year_from_file


class GetYearTestCase(unittest.TestCase):
    def test_given_valid_year_in_file_name_them_year_is_found(self) -> None:
        test_year_1 = 1900
        test_data_1 = Path(f"test/path/my_test_file_{test_year_1}.txt")
        expected_year_1 = 1900
        result_1 = get_year_from_file(test_data_1)

        test_year_2 = 1877
        test_data_2 = Path(f"test/path/my_test_file_{test_year_2}.txt")
        expected_year_2 = 1877
        result_2 = get_year_from_file(test_data_2)

        expected = [expected_year_1, expected_year_2]
        actual = [result_1, result_2]

        self.assertEqual(expected, actual)

    def test_given_not_valid_year_in_file_name_then_0_is_returned(self) -> None:
        test_year = 2020
        test_data = Path(f"test/path/my_test_file_{test_year}.txt")
        expected_year = 0
        result = get_year_from_file(test_data)

        self.assertEqual(expected_year, result)

    def test_given_no_match_in_file_name_then_0_is_returned(self) -> None:
        test_data = Path("test/path/my_test_file.txt")
        expected_year = 0
        result = get_year_from_file(test_data)

        self.assertEqual(expected_year, result)
