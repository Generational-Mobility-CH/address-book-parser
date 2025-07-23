from modules.persons.src.standardizer.constants.street_name_suffix_replacements import (
    STREET_NAME_SUFFIXES_MAP,
    STREET_NAME_SUFFIXES_EXCLUSIONS,
)
from modules.persons.src.util.regex.substitute_with_map import substitute_with_map

STREET_NAME_SUFFIXES_PATTERN_FORMAT = r"{PLACEHOLDER}$"


def standardize_street_name(text: str) -> str:
    text = text.replace(".", "").strip()

    if any(suffix in text.lower() for suffix in STREET_NAME_SUFFIXES_EXCLUSIONS):
        return text

    text = substitute_with_map(
        text, STREET_NAME_SUFFIXES_MAP, STREET_NAME_SUFFIXES_PATTERN_FORMAT
    )

    return text
