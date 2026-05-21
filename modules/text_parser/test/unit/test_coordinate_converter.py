import unittest

from modules.text_parser.src.coordinate_converter import wgs84_to_lv95


class CoordinateConverterTest(unittest.TestCase):
    def test_wgs84_to_lv95_ackerstrasse_20(self):
        """Cross-reference against known LV95 values from the LV95 lookup file."""
        easting, northing = wgs84_to_lv95(47.5783, 7.589)
        # Known LV95 values: northing=1269746.369, easting=2611316.782
        self.assertAlmostEqual(easting, 2611316.782, delta=5.0)
        self.assertAlmostEqual(northing, 1269746.369, delta=5.0)

    def test_wgs84_to_lv95_ackerstrasse_25(self):
        """Second cross-reference point."""
        easting, northing = wgs84_to_lv95(47.5784, 7.5893)
        # Known LV95 values: northing=1269758.87, easting=2611334.383
        self.assertAlmostEqual(easting, 2611334.383, delta=5.0)
        self.assertAlmostEqual(northing, 1269758.87, delta=5.0)

    def test_wgs84_to_lv95_returns_tuple(self):
        result = wgs84_to_lv95(47.5783, 7.589)
        self.assertIsInstance(result, tuple)
        self.assertEqual(len(result), 2)
