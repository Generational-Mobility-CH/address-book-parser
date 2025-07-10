import unittest

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.__main__ import main


class TemplateBugReproductionTestCase(unittest.TestCase):
    def test_bug(self):
        test_input = "../test/system/template_bug_reproduction/fixtures"
        test_output = "system/template_bug_reproduction/test_output.csv"
        column_names = [
            "original_names",
            "last_names",
            "first_names",
            # "job",
            # "address",
            # "year",
            # "pdf_page_number",
        ]

        main(test_input, test_output, SupportedFileTypes.CSV, column_names)


if __name__ == "__main__":
    unittest.main()
