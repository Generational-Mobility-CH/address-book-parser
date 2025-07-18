import re

from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement


def apply_regex_patterns(
    text: str, patterns_collection: list[PatternAndReplacement]
) -> str:
    for element in patterns_collection:
        text = re.sub(element.pattern, element.replacement, text)

    return text
