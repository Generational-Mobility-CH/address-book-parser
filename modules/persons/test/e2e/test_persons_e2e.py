import unittest

from modules.persons.src.__main__ import main


class PersonsE2ETestCase(unittest.TestCase):
    def test_main(self):
        demo_input_path = "fixtures/input/json"
        demo_output_path = "fixtures/output/e2e_test.db"

        main(demo_input_path, demo_output_path)
