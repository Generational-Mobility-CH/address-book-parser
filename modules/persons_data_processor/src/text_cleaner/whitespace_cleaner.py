import re

from modules.persons_data_processor.src.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)

WHITESPACE_PATTERN = re.compile(r"\s+")
LEADING_WHITESPACE_PATTERN = re.compile(r"^\s+")
TRAILING_WHITESPACE_PATTERN = re.compile(r"\s+$")

WHITESPACE_PATTERNS_AND_REPL: list[PatternAndRepl] = [
    (WHITESPACE_PATTERN, " "),
    (LEADING_WHITESPACE_PATTERN, ""),
    (TRAILING_WHITESPACE_PATTERN, ""),
]
