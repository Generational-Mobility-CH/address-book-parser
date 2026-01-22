import re

from modules.text_cleaner.src.constants.allowed_special_characters import (
    ALLOWED_SPECIAL_CHARACTERS,
)
from modules.text_cleaner.src.constants.unallowed_strings import (
    UNALLOWED_STRINGS,
    UNALLOWED_AT_START_OF_STRING,
)
from modules.text_cleaner.src.types.pattern_and_repl_type import PatternAndRepl

UNALLOWED_STRINGS_PATTERN = re.compile(
    rf"({'|'.join(map(re.escape, UNALLOWED_STRINGS))})"
)
UNALLOWED_AT_START_OF_STRING_PATTERN = re.compile(
    rf"^({'|'.join(map(re.escape, UNALLOWED_AT_START_OF_STRING))})"
)
ALLOWED_SPECIAL_CHARACTERS_PATTERN = re.compile(
    rf"[^\w{re.escape(''.join(ALLOWED_SPECIAL_CHARACTERS))}]"
)

UNALLOWED_STRINGS_PATTERNS_AND_REPL: list[PatternAndRepl] = [
    (UNALLOWED_AT_START_OF_STRING_PATTERN, ""),
    (UNALLOWED_STRINGS_PATTERN, ""),
    (ALLOWED_SPECIAL_CHARACTERS_PATTERN, ""),
]
