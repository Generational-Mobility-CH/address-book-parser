import unittest

from src.text_parser.src.prefix_extractor import (
    extract_entry_symbols,
    extract_title_prefix,
)


class TestExtractEntrySymbols(unittest.TestCase):
    def test_both_symbols(self):
        tel, post, line = extract_entry_symbols("\u25cf\u2021\u2014 -Weber Richard")
        self.assertTrue(tel)
        self.assertTrue(post)
        self.assertEqual(line, "\u2014 -Weber Richard")

    def test_dagger_only(self):
        tel, post, line = extract_entry_symbols("\u2021\u2014M\u00fcller Fritz")
        self.assertTrue(tel)
        self.assertFalse(post)
        self.assertEqual(line, "\u2014M\u00fcller Fritz")

    def test_bullet_only(self):
        tel, post, line = extract_entry_symbols("\u25cfBauer Hans")
        self.assertFalse(tel)
        self.assertTrue(post)
        self.assertEqual(line, "Bauer Hans")

    def test_no_symbols(self):
        tel, post, line = extract_entry_symbols("Schneider Karl")
        self.assertFalse(tel)
        self.assertFalse(post)
        self.assertEqual(line, "Schneider Karl")

    def test_em_dash_not_treated_as_symbol(self):
        tel, post, line = extract_entry_symbols("\u2014 -Zimmer Anna")
        self.assertFalse(tel)
        self.assertFalse(post)
        self.assertEqual(line, "\u2014 -Zimmer Anna")

    def test_symbols_with_space(self):
        tel, post, line = extract_entry_symbols("\u25cf\u2021 \u2014Name")
        self.assertTrue(tel)
        self.assertTrue(post)
        self.assertEqual(line, "\u2014Name")


class TestExtractTitlePrefix(unittest.TestCase):
    def test_dr(self):
        prefix, name = extract_title_prefix("Dr. Karl")
        self.assertEqual(prefix, "Dr.")
        self.assertEqual(name, "Karl")

    def test_dr_med(self):
        prefix, name = extract_title_prefix("Dr. Med. Karl")
        self.assertEqual(prefix, "Dr. Med.")
        self.assertEqual(name, "Karl")

    def test_dr_phil(self):
        prefix, name = extract_title_prefix("Dr. Phil. Eugen")
        self.assertEqual(prefix, "Dr. Phil.")
        self.assertEqual(name, "Eugen")

    def test_wwe(self):
        prefix, name = extract_title_prefix("Wwe. Anna")
        self.assertEqual(prefix, "Wwe.")
        self.assertEqual(name, "Anna")

    def test_frau(self):
        prefix, name = extract_title_prefix("Frau Hedwig")
        self.assertEqual(prefix, "Frau")
        self.assertEqual(name, "Hedwig")

    def test_prof(self):
        prefix, name = extract_title_prefix("Prof. Hans")
        self.assertEqual(prefix, "Prof.")
        self.assertEqual(name, "Hans")

    def test_no_prefix(self):
        prefix, name = extract_title_prefix("Karl")
        self.assertEqual(prefix, "")
        self.assertEqual(name, "Karl")

    def test_empty(self):
        prefix, name = extract_title_prefix("")
        self.assertEqual(prefix, "")
        self.assertEqual(name, "")

    def test_dr_without_specialization(self):
        prefix, name = extract_title_prefix("Dr. Alfred")
        self.assertEqual(prefix, "Dr.")
        self.assertEqual(name, "Alfred")


if __name__ == "__main__":
    unittest.main()
