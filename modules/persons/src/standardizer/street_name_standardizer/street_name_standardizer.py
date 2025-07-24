from logging import getLogger

from rapidfuzz import process

from modules.persons.src.standardizer.street_name_standardizer.constants.common_misspelled_street_names import (
    COMMON_MISSPELLED_STREET_NAMES_MAP,
)
from modules.persons.src.standardizer.street_name_standardizer.constants.historical_street_names_basel import (
    HISTORICAL_STREET_NAMES_BASEL,
)
from modules.persons.src.standardizer.street_name_standardizer.constants.street_name_suffixes_abbreviations import (
    STREET_NAME_SUFFIXES_ABBREVIATION_MAP,
)
from modules.persons.src.standardizer.street_name_standardizer.constants.street_name_suffixes import (
    STREET_NAME_SUFFIXES,
)
from modules.persons.src.util.regex.substitute_with_map import substitute_with_map

logger = getLogger(__name__)


def normalize_street_name(text: str) -> str:
    text = text.replace(".", "").strip()

    if any(suffix in text.lower() for suffix in STREET_NAME_SUFFIXES):
        return text

    text = substitute_with_map(
        text, STREET_NAME_SUFFIXES_ABBREVIATION_MAP, r"{PLACEHOLDER}$"
    )

    return text


def correct_spelling(
    word: str, threshold: int = 80, word_list=HISTORICAL_STREET_NAMES_BASEL
) -> str | None:
    match = process.extractOne(word, word_list, score_cutoff=threshold)

    return match[0] if match else None


def fix_spelling(text: str) -> str:
    if corrected_text := correct_spelling(text):
        return corrected_text

    if text in COMMON_MISSPELLED_STREET_NAMES_MAP:
        return COMMON_MISSPELLED_STREET_NAMES_MAP[text]

    return f"{text}<TODO FIX SPELLING>"


def standardize_street_name(text: str) -> str:
    text = normalize_street_name(text)

    if text not in HISTORICAL_STREET_NAMES_BASEL:
        return fix_spelling(text)

    return text
