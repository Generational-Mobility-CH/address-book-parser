import re

from modules.persons.src.standardizer.constants.street_name_suffix_replacements import (
    suffix_replacements,
    suffix_exceptions,
)


def standardize_street_name(text: str) -> str:
    text = replace_street_suffix(text)

    return text


def replace_street_suffix(text: str) -> str:
    text = text.replace(".", "")

    if any(suffix in text.lower() for suffix in suffix_exceptions):
        return text

    for abbrev, full in suffix_replacements.items():
        if re.search(abbrev, text):
            return re.sub(abbrev, full, text)

    return text
