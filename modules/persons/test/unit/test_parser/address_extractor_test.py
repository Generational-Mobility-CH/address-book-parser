import unittest

from modules.persons.models.person.address import Address
from modules.persons.src.parser.address_parser import extract_address


class AddressExtractorTest(unittest.TestCase):
    def test_extract_address(self) -> None:
        test_input = [
            "Bahnhofstr. 10",
            "23 Gehweg",
            "Wohnblock an der Main 30c",
            "30 Homburgerstrasse.",
        ]

        expected_output = [
            Address(street_name="Bahnhofstr.", house_number="10"),
            Address(street_name="Gehweg", house_number="23"),
            Address(street_name="Wohnblock an der Main", house_number="30c"),
            Address(street_name="Homburgerstrasse.", house_number="30"),
        ]

        actual_output = [extract_address(s) for s in test_input]

        for i, (actual, expected) in enumerate(zip(actual_output, expected_output)):
            self.assertEqual(
                actual,
                expected,
                f"\n\nMismatch at list element nr. {i + 1}: '{actual}' != '{expected}'",
            )
