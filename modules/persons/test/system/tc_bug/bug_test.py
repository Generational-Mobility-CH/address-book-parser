import unittest

from libs.file_handler.src.models.supported_file_types import SupportedFileTypes
from modules.persons.src.__main__ import main
from modules.persons.src.parser.text_sanitizer import sanitize_line


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test_input = "../test/system/tc_bug/fixtures"
        test_output = "system/tc_bug/test_output.csv"

        main(test_input, test_output, SupportedFileTypes.CSV)

    def test_something2(self):
        test_input = "Galliaith ½ — -Göpfert Hans"
        expected = "Galliaith-Göpfert Hans"
        # TODO check case: -Göpfert am Anfang

        actual = sanitize_line(test_input)

        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
