import logging

from modules.persons.src.models.address_book.name_range import NameRange
from modules.persons.src.parser.names.constants.german_vowels import GERMAN_UMLAUTE
from modules.persons.src.parser.names.constants.names_special_keywords import (
    PLACEHOLDERS_LAST_NAME,
)

logger = logging.getLogger(__name__)


def extract_other_names(text: str) -> str:
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


def get_last_name(text: str) -> str:
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


def is_name(text: str, last_name: str) -> bool:
    return last_name in text or any(
        placeholder in text for placeholder in PLACEHOLDERS_LAST_NAME
    )


def prepare_str_for_comparison(text: str) -> str:
    text = text.strip()
    text = replace_if_contains_umlaute(text)
    text = text.lower()

    return text


def is_valid_next_last_name(current: str, last_name_range: NameRange) -> bool:
    current = prepare_str_for_comparison(current)
    current = get_last_name(current)
    start = prepare_str_for_comparison(last_name_range.start)
    end = prepare_str_for_comparison(last_name_range.end)

    return start <= current <= end


def is_valid_next_last_name_legacy(current: str, previous: str) -> bool:
    current = prepare_str_for_comparison(current)
    current = get_last_name(current)
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


def get_next_last_name(
    all_names: str, current_last_name: str, last_names_range: NameRange
) -> tuple[str, str]:
    if not current_last_name:
        found_last_name = get_last_name(all_names)
        current_last_name = (
            found_last_name
            if is_valid_next_last_name(found_last_name, last_names_range)
            else last_names_range.start
        )

    if starts_with_last_name_placeholder(all_names):
        all_names = current_last_name + extract_other_names(all_names)
    elif is_valid_next_last_name(all_names, last_names_range):
        current_last_name = get_last_name(all_names)
    else:
        all_names = f"{current_last_name} {all_names}"

    return all_names, current_last_name


def get_next_last_name_without_range(
    all_names: str, current_last_name: str, previous_last_name: str
) -> tuple[str, str, str]:
    if not current_last_name and not previous_last_name:
        previous_last_name = current_last_name = get_last_name(all_names)
    elif is_valid_next_last_name_legacy(all_names, previous_last_name):
        previous_last_name, current_last_name = (
            current_last_name,
            get_last_name(all_names),
        )

    if starts_with_last_name_placeholder(all_names):
        all_names = current_last_name + extract_other_names(all_names)
    elif all_names.startswith("("):
        all_names = current_last_name + " " + all_names

    return all_names, current_last_name, previous_last_name


def contains_umlaute(input_string: str) -> bool:
    return any(char in GERMAN_UMLAUTE for char in input_string.lower())


def replace_umlaute(text: str) -> str:
    return "".join(GERMAN_UMLAUTE.get(char, char) for char in text.lower()).title()


def replace_if_contains_umlaute(text: str) -> str:
    return replace_umlaute(text) if contains_umlaute(text) else text


def starts_with_last_name_placeholder(text: str) -> bool:
    return bool(text) and text[0] in PLACEHOLDERS_LAST_NAME
