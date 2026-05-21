import unittest

from modules.shared.models.address import Address
from modules.text_parser.src.address_parser import (
    add_coordinates,
    extract_address,
)


class AddressParserTest(unittest.TestCase):
    def test_extract_address(self) -> None:
        test_cases = [
            (
                "Bahnhofstr. 10",
                Address(street_name="Bahnhofstr.", house_number="10", coordinates=None),
            ),
            (
                "23 Gehweg",
                Address(street_name="Gehweg", house_number="23", coordinates=None),
            ),
            (
                "Wohnblock an der Main 30c",
                Address(
                    street_name="Wohnblock an der Main",
                    house_number="30c",
                    coordinates=None,
                ),
            ),
            (
                "30 Homburgerstrasse.",
                Address(
                    street_name="Homburgerstrasse.", house_number="30", coordinates=None
                ),
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

    def test_add_coordinates_known_address(self):
        address = Address(street_name="Ackerstrasse", house_number="20", coordinates=None)
        result = add_coordinates(address)
        self.assertIsNotNone(result.coordinates)
        self.assertAlmostEqual(result.coordinates.latitude_wgs84, 47.5783)
        self.assertAlmostEqual(result.coordinates.longitude_wgs84, 7.589)
        self.assertAlmostEqual(result.coordinates.easting_lv95, 2611316.782, delta=5.0)
        self.assertAlmostEqual(result.coordinates.northing_lv95, 1269746.369, delta=5.0)

    def test_add_coordinates_unknown_address(self):
        address = Address(street_name="Nonexistent", house_number="999", coordinates=None)
        result = add_coordinates(address)
        self.assertIsNone(result.coordinates)
