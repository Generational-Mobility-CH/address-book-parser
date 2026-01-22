import re

from modules.text_cleaner.src.types.pattern_and_repl_type import PatternAndRepl


def apply_regex_patterns(text: str, patterns_collection: list[PatternAndRepl]) -> str:
    for element in patterns_collection:
        text = re.sub(element[0], element[1], text)

    return text
