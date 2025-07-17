import unittest

from modules.persons.src.cleaner.text_cleaner.text_cleaner import clean_text_lines


class TextCleanerTestCase(unittest.TestCase):
    def test_clean_text_lines(self) -> None:
        test_cases = [
            ("Siegmann-| Höfer Trangott\n", "Siegmann-Höfer Trangott"),
            ("½ — Suppiger ", "-Suppiger"),
            ("fractext  f text  f -Vischer Theod.", "f-Vischer Theod."),
            ("Märklin fractext text — Jaecck Alfr.", "Märklin-Jaecck Alfr."),
        ]

        actual_output = clean_text_lines([tc[0] for tc in test_cases])

        for i, (actual, (_, expected)) in enumerate(zip(actual_output, test_cases)):
            with self.subTest(i=i, input=test_cases[i][0]):
                self.assertEqual(
                    actual,
                    expected,
                    f"\n\nMismatch at case #{i + 1}:\n'{actual}' != '{expected}'",
                )
