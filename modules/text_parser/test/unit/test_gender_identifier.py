import unittest

from modules.text_parser.src.gender_identifier import (
    found_female_first_name,
    found_male_first_name,
)


class GenderIdentificationTestCase(unittest.TestCase):
    def test_female_name_found(self):
        self.assertEqual(True, found_female_first_name("Adeline"))

    def test_male_name_found(self):
        self.assertEqual(True, found_male_first_name("Gust."))
