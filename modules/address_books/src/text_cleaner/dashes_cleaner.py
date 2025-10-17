import re

from modules.address_books.src.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)

STANDARDIZE_DASHES_AND_WHITESPACE = re.compile(r"\s*—\s*|\s*-\s*")
REPEATED_DASHES = re.compile(r"-{2,}")

DASHES_PATTERNS_AND_REPL: list[PatternAndRepl] = [
    (STANDARDIZE_DASHES_AND_WHITESPACE, "-"),
    (REPEATED_DASHES, "-"),
]
