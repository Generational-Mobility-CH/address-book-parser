import re

from modules.address_books.parser.src.cleaner.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)

GERMAN_ALPHABET = "a-zA-ZäöüÄÖÜß"

LOWER_CASE_FOLLOWED_BY_UPPER_CASE = re.compile(r"([a-zäöü])([A-ZÄÖÜ])")
DOT_FOLLOWED_BY_LETTER = re.compile(rf"([{GERMAN_ALPHABET}]\.)([{GERMAN_ALPHABET}])")
NO_SPACE_BEFORE_PARENTHESIS = re.compile(rf"([{GERMAN_ALPHABET}^-])(\()")
NO_SPACE_AFTER_PARENTHESIS = re.compile(rf"(\))([{GERMAN_ALPHABET}^-])")

SEPARATE_WORDS_PATTERNS_AND_REPL: list[PatternAndRepl] = [
    (LOWER_CASE_FOLLOWED_BY_UPPER_CASE, r"\1 \2"),
    (DOT_FOLLOWED_BY_LETTER, r"\1 \2"),
    (NO_SPACE_BEFORE_PARENTHESIS, r"\1 \2"),
    (NO_SPACE_AFTER_PARENTHESIS, r"\1 \2"),
]
