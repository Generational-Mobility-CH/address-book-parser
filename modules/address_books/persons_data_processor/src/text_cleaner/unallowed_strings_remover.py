import re

from modules.address_books.persons_data_processor.src.text_cleaner.constants.allowed_special_characters import (
    ALLOWED_SPECIAL_CHARACTERS,
)
from modules.address_books.persons_data_processor.src.text_cleaner.constants.unallowed_strings import (
    UNALLOWED_STRINGS,
    UNALLOWED_AT_START_OF_STRING,
)
from modules.address_books.persons_data_processor.src.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)

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
