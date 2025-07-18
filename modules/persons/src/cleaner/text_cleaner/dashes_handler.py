import re


from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement


STANDARDIZE_DASHES_AND_WHITESPACE = re.compile(r"\s*—\s*|\s*-\s*")
REPEATED_DASHES = re.compile(r"-{2,}")

DASHES_PATTERNS_AND_REPLACEMENT: list[PatternAndReplacement] = [
    PatternAndReplacement(pattern=STANDARDIZE_DASHES_AND_WHITESPACE, replacement="-"),
    PatternAndReplacement(pattern=REPEATED_DASHES, replacement="-"),
]
