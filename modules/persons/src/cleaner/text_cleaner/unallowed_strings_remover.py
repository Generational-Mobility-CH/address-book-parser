import re

from modules.persons.src.cleaner.text_cleaner.constants.allowed_special_characters import (
    ALLOWED_SPECIAL_CHARACTERS,
)
from modules.persons.src.cleaner.text_cleaner.constants.unallowed_strings import (
    UNALLOWED_AT_START_OF_STRING,
    UNALLOWED_STRINGS,
)
from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement

START_PATTERN = re.compile(
    rf"^({'|'.join(map(re.escape, UNALLOWED_AT_START_OF_STRING))})"
)
UNALLOWED_PATTERN = re.compile(rf"({'|'.join(map(re.escape, UNALLOWED_STRINGS))})")
CLEAN_PATTERN = re.compile(rf"[^\w{re.escape(''.join(ALLOWED_SPECIAL_CHARACTERS))}]")

UNALLOWED_STRINGS_PATTERNS_AND_REPLACEMENT: list[PatternAndReplacement] = [
    PatternAndReplacement(pattern=START_PATTERN, replacement=""),
    PatternAndReplacement(pattern=UNALLOWED_PATTERN, replacement=""),
    PatternAndReplacement(pattern=CLEAN_PATTERN, replacement=""),
]
