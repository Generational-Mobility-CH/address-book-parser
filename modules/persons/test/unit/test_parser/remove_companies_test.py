import unittest

from modules.persons.src.parser.company_parser import is_company


class MyTestCase(unittest.TestCase):
    def test_remove_companies(self):
        test_file = "fixtures/test_input.txt"
        expected_output = [
            "— -Neukomm Emil, Kfm., 44 Elisabethenstr. (Frau: Damenschneiderin.)\n",
            "— -Ritter Ad., Buchh., 47 Delsbergerallee.\n",
        ]
        actual_output = []

        with open(test_file, "r") as f:
            for line in f.readlines():
                information = line.split(",")
                if is_company(information):
                    continue
                actual_output.append(line)

        self.assertEqual(expected_output, actual_output)
