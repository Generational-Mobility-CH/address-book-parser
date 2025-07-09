import unittest

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.__main__ import main


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test_input = "../test/system/template_bug_reproduction/fixtures"
        test_output = "system/template_bug_reproduction/test_output.csv"

        main(test_input, test_output, SupportedFileTypes.CSV)


if __name__ == "__main__":
    unittest.main()
