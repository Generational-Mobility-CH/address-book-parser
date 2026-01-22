from logging import getLogger

from fuzzywuzzy import process

from modules.text_parser.src.constants.tags import TAG_NONE_FOUND
from modules.text_standardizer.src.constants.street_names.corrected_street_names import (
    CORRECTED_STREET_NAMES_MAP,
)
from modules.text_standardizer.src.constants.street_names.historical_street_names_basel import (
    HISTORICAL_STREET_NAMES_BASEL,
)
from modules.text_standardizer.src.constants.street_names.street_name_prefixes import (
    STREET_NAME_PREFIXES_ABBREVIATION_MAP,
)
from modules.text_standardizer.src.constants.street_names.street_name_suffixes import (
    STREET_NAME_SUFFIXES,
    STREET_NAME_SUFFIXES_ABBREVIATION_MAP,
)
from libs.regex.src.substitute_with_map import (
    substitute_with_map,
)

logger = getLogger(__name__)


def standardize_street_name_suffixes_and_prefixes(text: str) -> str:
    text = text.replace(".", "").strip().lower()

    text = substitute_with_map(
        text, STREET_NAME_PREFIXES_ABBREVIATION_MAP, r"^{PLACEHOLDER}\b"
    )

    if text.startswith("st "):
        text = text.replace("st ", "St. ")

    if any(text.endswith(suffix) for suffix in STREET_NAME_SUFFIXES):
        return text.title()

    text = substitute_with_map(
        text, STREET_NAME_SUFFIXES_ABBREVIATION_MAP, r"{PLACEHOLDER}$"
    )

    return text.title()


def get_fuzzy_match(word: str) -> str | None:
    threshold = 70
    word = word.lower()
    match = process.extractOne(
        word, HISTORICAL_STREET_NAMES_BASEL, score_cutoff=threshold
    )

    return match[0] if match else None


def fix_spelling(text: str) -> str:
    if text in CORRECTED_STREET_NAMES_MAP:
        return CORRECTED_STREET_NAMES_MAP[text]

    if corrected_text := get_fuzzy_match(text):
        return corrected_text

    return f"{text}<TODO FIX SPELLING>"


def standardize_street_name(text: str) -> str:
    text = standardize_street_name_suffixes_and_prefixes(text)

    if (
        bool(text)
        and text not in HISTORICAL_STREET_NAMES_BASEL
        and text.lower() != TAG_NONE_FOUND.lower()
    ):
        return fix_spelling(text)

    return text
