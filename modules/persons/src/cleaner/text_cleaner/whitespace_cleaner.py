import re

from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement

WHITESPACE_PATTERN = re.compile(r"\s+")
LEADING_WHITESPACE_PATTERN = re.compile(r"^\s+")
TRAILING_WHITESPACE_PATTERN = re.compile(r"\s+$")
WHITESPACE_PATTERNS_AND_REPLACEMENT: list[PatternAndReplacement] = [
    PatternAndReplacement(pattern=WHITESPACE_PATTERN, replacement=" "),
    PatternAndReplacement(pattern=LEADING_WHITESPACE_PATTERN, replacement=""),
    PatternAndReplacement(pattern=TRAILING_WHITESPACE_PATTERN, replacement=""),
]
