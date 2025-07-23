from logging import getLogger

from rapidfuzz import process

from modules.persons.src.standardizer.street_name_standardizer.constants.historical_street_names_basel import (
    HISTORICAL_STREET_NAMES_BASEL,
)
from modules.persons.src.standardizer.street_name_standardizer.constants.street_name_suffix_replacements import (
    STREET_NAME_SUFFIXES_EXCLUSIONS,
    STREET_NAME_SUFFIXES_MAP,
)
from modules.persons.src.util.regex.substitute_with_map import substitute_with_map

logger = getLogger(__name__)

STREET_NAME_SUFFIXES_PATTERN_FORMAT = r"{PLACEHOLDER}$"


def standardize_street_name(text: str) -> str:
    text = normalize_street_name(text)

    if text not in HISTORICAL_STREET_NAMES_BASEL:
        return correct_spelling(text)

    return text


def normalize_street_name(text: str) -> str:
    text = text.replace(".", "").strip()

    if any(suffix in text.lower() for suffix in STREET_NAME_SUFFIXES_EXCLUSIONS):
        return text

    text = substitute_with_map(
        text, STREET_NAME_SUFFIXES_MAP, STREET_NAME_SUFFIXES_PATTERN_FORMAT
    )

    return text


def correct_spelling(word: str, threshold: int = 80) -> str | None:
    word_list = HISTORICAL_STREET_NAMES_BASEL
    match = process.extractOne(word, word_list, score_cutoff=threshold)
    return match[0] if match else None
