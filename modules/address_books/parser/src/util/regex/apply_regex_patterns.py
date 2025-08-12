import re

from modules.address_books.parser.src.cleaner.text_cleaner.types.pattern_and_repl_type import (
    PatternAndRepl,
)


def apply_regex_patterns(text: str, patterns_collection: list[PatternAndRepl]) -> str:
    for element in patterns_collection:
        text = re.sub(element[0], element[1], text)

    return text
