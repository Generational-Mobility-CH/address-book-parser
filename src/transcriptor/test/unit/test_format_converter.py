import unittest

from src.transcriptor.src.api_dots_ocr.format_converter import (
    convert_to_raw_lines,
    count_entries,
)


class TestConvertToRawLines(unittest.TestCase):
    """Test conversion from P10v output to raw lines.

    format_converter now preserves \u25cf and \u2021 symbols so the parser
    can extract telephone/postcheck booleans downstream.
    """

    def test_full_prefix_with_partner_dash(self):
        """\u25cf\u2021\u2014 - prefix: preserve all symbols, strip number only."""
        text = "1. \u25cf\u2021\u2014 -Weber Richard, Redaktor, 89 Gotthardstr."
        result = convert_to_raw_lines(text)
        self.assertEqual(
            result, "\u25cf\u2021\u2014 -Weber Richard, Redaktor, 89 Gotthardstr."
        )

    def test_dagger_with_em_dash(self):
        """\u2021\u2014 prefix: preserve dagger and em-dash."""
        text = "2. \u2021\u2014M\u00fcller Fritz, Schlosser, 12 Spalenberg."
        result = convert_to_raw_lines(text)
        self.assertEqual(
            result, "\u2021\u2014M\u00fcller Fritz, Schlosser, 12 Spalenberg."
        )

    def test_partner_dash_without_symbols(self):
        """\u2014 - prefix without bullet/dagger: preserve as-is."""
        text = "3. \u2014 -Zimmer Anna, Wwe., 5 Freiestr."
        result = convert_to_raw_lines(text)
        self.assertEqual(result, "\u2014 -Zimmer Anna, Wwe., 5 Freiestr.")

    def test_em_dash_only(self):
        """\u2014 prefix only: preserve."""
        text = "4. \u2014Name Fritz, B\u00e4cker, 7 Gerbergasse."
        result = convert_to_raw_lines(text)
        self.assertEqual(
            result, "\u2014Name Fritz, B\u00e4cker, 7 Gerbergasse."
        )

    def test_plain_entry(self):
        """No prefix symbols: just strip number."""
        text = "5. Schneider Karl, B\u00e4cker, 7 Gerbergasse."
        result = convert_to_raw_lines(text)
        self.assertEqual(result, "Schneider Karl, B\u00e4cker, 7 Gerbergasse.")

    def test_bullet_dagger_no_dash(self):
        """\u25cf\u2021 prefix without dash: preserve symbols."""
        text = "1. \u25cf\u2021Bauer Hans, Kaufmann, 3 Marktplatz."
        result = convert_to_raw_lines(text)
        self.assertEqual(result, "\u25cf\u2021Bauer Hans, Kaufmann, 3 Marktplatz.")

    def test_multiline(self):
        """Multiple entries separated by newlines."""
        text = (
            "1. \u25cf\u2021\u2014 -Weber Richard, Redaktor, 89 Gotthardstr.\n"
            "2. \u2021\u2014M\u00fcller Fritz, Schlosser, 12 Spalenberg.\n"
            "3. \u2014Anna, Wwe.\n"
            "4. Schneider Karl, B\u00e4cker, 7 Gerbergasse."
        )
        result = convert_to_raw_lines(text)
        expected = (
            "\u25cf\u2021\u2014 -Weber Richard, Redaktor, 89 Gotthardstr.\n"
            "\u2021\u2014M\u00fcller Fritz, Schlosser, 12 Spalenberg.\n"
            "\u2014Anna, Wwe.\n"
            "Schneider Karl, B\u00e4cker, 7 Gerbergasse."
        )
        self.assertEqual(result, expected)

    def test_empty_lines_stripped(self):
        """Empty lines between entries are removed."""
        text = "1. Name One\n\n2. Name Two\n\n"
        result = convert_to_raw_lines(text)
        self.assertEqual(result, "Name One\nName Two")

    def test_empty_input(self):
        """Empty string returns empty string."""
        self.assertEqual(convert_to_raw_lines(""), "")
        self.assertEqual(convert_to_raw_lines("  \n  "), "")


class TestCountEntries(unittest.TestCase):
    def test_count(self):
        text = "line 1\nline 2\nline 3"
        self.assertEqual(count_entries(text), 3)

    def test_empty(self):
        self.assertEqual(count_entries(""), 0)
        self.assertEqual(count_entries("  \n  "), 0)


if __name__ == "__main__":
    unittest.main()
