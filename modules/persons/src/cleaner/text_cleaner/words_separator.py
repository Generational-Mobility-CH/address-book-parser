import re

from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement

GERMAN_ALPHABET = "a-zA-ZäöüÄÖÜß"

LOWER_CASE_FOLLOWED_BY_UPPER_CASE = re.compile(r"([a-zäöü])([A-ZÄÖÜ])")
DOT_FOLLOWED_BY_LETTER = re.compile(rf"([{GERMAN_ALPHABET}]\.)([{GERMAN_ALPHABET}])")
NO_SPACE_BEFORE_PARENTHESIS = re.compile(rf"([{GERMAN_ALPHABET}^-])(\()")
NO_SPACE_AFTER_PARENTHESIS = re.compile(rf"(\))([{GERMAN_ALPHABET}^-])")

SEPARATE_WORDS_PATTERNS_AND_REPLACEMENT: list[PatternAndReplacement] = [
    PatternAndReplacement(
        pattern=LOWER_CASE_FOLLOWED_BY_UPPER_CASE, replacement=r"\1 \2"
    ),
    PatternAndReplacement(pattern=DOT_FOLLOWED_BY_LETTER, replacement=r"\1 \2"),
    PatternAndReplacement(pattern=NO_SPACE_BEFORE_PARENTHESIS, replacement=r"\1 \2"),
    PatternAndReplacement(pattern=NO_SPACE_AFTER_PARENTHESIS, replacement=r"\1 \2"),
]
