import unittest

from modules.panel_data.src.gender_calculator.gender_calculator import (
    found_female_first_name,
)


class MyTestCase(unittest.TestCase):
    def test_female_name_found(self):
        answer = found_female_first_name("Adeline")

        self.assertEqual(True, answer)
