import unittest

from modules.persons_data_processor.src.models.person.address import (
    Address,
)
from modules.persons_data_processor.src.parser.address_parser import (
    extract_address,
)


class AddressParserTest(unittest.TestCase):
    def test_extract_address(self) -> None:
        test_cases = [
            ("Bahnhofstr. 10", Address(street_name="Bahnhofstr.", house_number="10")),
            ("23 Gehweg", Address(street_name="Gehweg", house_number="23")),
            (
                "Wohnblock an der Main 30c",
                Address(street_name="Wohnblock an der Main", house_number="30c"),
            ),
            (
                "30 Homburgerstrasse.",
                Address(street_name="Homburgerstrasse.", house_number="30"),
            ),
        ]

        for i, (input_str, expected) in enumerate(test_cases):
            with self.subTest(i=i, input=input_str):
                actual = extract_address(input_str)
                self.assertEqual(
                    actual,
                    expected,
                    f"\nMismatch at test case #{i + 1}: '{actual}' != '{expected}'",
                )
