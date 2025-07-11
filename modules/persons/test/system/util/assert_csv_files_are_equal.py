import csv
import os


def assert_csv_files_are_equal(expected_file: str, test_output: str):
    with (
        open(expected_file, newline="") as expected,
        open(test_output, newline="") as actual,
    ):
        reader = csv.DictReader(actual)
        actual_lines = set(
            tuple((k, v.strip()) for k, v in row.items()) for row in reader
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
            raise AssertionError("CSV files differ")
        else:
            os.remove(test_output)
