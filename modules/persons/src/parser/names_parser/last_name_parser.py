import logging

from modules.persons.src.models.address_book.name_range import NameRange
from modules.persons.src.parser.names_parser.constants.german_vowels import (
    GERMAN_UMLAUTE,
)
from modules.persons.src.parser.names_parser.constants.names_special_keywords import (
    PLACEHOLDERS_LAST_NAME,
)

logger = logging.getLogger(__name__)


def _is_valid_next_last_name(current: str, name_range: NameRange) -> bool:
    current = prepare_str_for_comparison(current)
    current = _find_last_name_in_str(current)
    start = prepare_str_for_comparison(name_range.start)
    end = prepare_str_for_comparison(name_range.end)

    return start <= current <= end


def _is_valid_next_last_name_legacy(current: str, previous: str) -> bool:
    current = prepare_str_for_comparison(current)
    current = _find_last_name_in_str(current)
    previous = prepare_str_for_comparison(previous)

    if not current or not previous:
        return False

    current_first_letter = current[0]
    previous_first_letter = previous[0]

    if current_first_letter == previous_first_letter:
        return True
    elif ord(current_first_letter) == ord(previous_first_letter) + 1:
        return True

    return False


def _contains_umlaute(input_string: str) -> bool:
    return any(char in GERMAN_UMLAUTE for char in input_string.lower())


def _replace_umlaute(text: str) -> str:
    return "".join(GERMAN_UMLAUTE.get(char, char) for char in text.lower()).title()


def _find_last_name_in_str(text: str) -> str:
    text = text.replace("—", "-")
    name_parts = [part for part in text.split() if part != "-"]

    if not name_parts:
        return text

    first_part = name_parts[0]

    if "-" in first_part:
        first_subparts = [p for p in first_part.split("-", 1) if bool(p)]
        if not first_subparts:
            logger.warning(f"Could not get last name from {text}")
            return text

        first_part = first_subparts[0]

    return first_part


def _extract_other_names(text: str) -> str:
    match text[1]:
        case _ if text[1].isalpha():
            result = " " + text[1:]
        case " ":
            if text[2] in PLACEHOLDERS_LAST_NAME:
                result = text[2:]
            else:
                result = text[1:]
        case _:
            result = text[1:]

    return result


def prepare_str_for_comparison(text: str) -> str:
    text = text.strip()
    text = _replace_umlaute(text) if _contains_umlaute(text) else text
    text = text.lower()

    return text


def get_next_last_name(
    all_names: str, current_last_name: str, last_names_range: NameRange
) -> tuple[str, str]:
    if not current_last_name:
        found_last_name = _find_last_name_in_str(all_names)
        current_last_name = (
            found_last_name
            if _is_valid_next_last_name(found_last_name, last_names_range)
            else last_names_range.start
        )

    if all_names.startswith(PLACEHOLDERS_LAST_NAME):
        all_names = current_last_name + _extract_other_names(all_names)
    elif _is_valid_next_last_name(all_names, last_names_range):
        current_last_name = _find_last_name_in_str(all_names)
    else:
        all_names = f"{current_last_name} {all_names}"

    return all_names, current_last_name


def get_next_last_name_without_range(
    all_names: str, current_last_name: str, previous_last_name: str
) -> tuple[str, str, str]:
    if not current_last_name and not previous_last_name:
        previous_last_name = current_last_name = _find_last_name_in_str(all_names)
    elif _is_valid_next_last_name_legacy(all_names, previous_last_name):
        previous_last_name, current_last_name = (
            current_last_name,
            _find_last_name_in_str(all_names),
        )

    if all_names.startswith(PLACEHOLDERS_LAST_NAME):
        all_names = current_last_name + _extract_other_names(all_names)
    elif all_names.startswith("("):
        all_names = current_last_name + " " + all_names

    return all_names, current_last_name, previous_last_name
