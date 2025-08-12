import csv
from pathlib import Path


def assert_csv_files_are_equal(expected_file: Path, test_output: Path):
    with (
        expected_file.open(newline="") as expected,
        test_output.open(newline="") as actual,
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
                print("\nMISSING:")
                for line in missing_lines:
                    print(f"{line}")
            if superfluous_lines:
                print("\nSUPERFLUOUS:")
                for line in superfluous_lines:
                    print(f"{line}")

            raise AssertionError("CSV files differ")
        else:
            test_output.unlink()
