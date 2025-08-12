import logging

from modules.address_books.parser.src.models.address_book.name_range import NameRange
from modules.address_books.parser.src.parser.constants.last_name_placeholders import (
    LAST_NAME_PLACEHOLDERS,
)
from modules.shared.util.prepare_str_for_comparison import prepare_str_for_comparison

logger = logging.getLogger(__name__)


def _find_last_name_in_str(text: str) -> str:
    text = text.replace("—", "-")
    name_parts = [part for part in text.split() if part != "-"]

    if not name_parts:
        return text

    first_part = name_parts[0]

    if "-" in first_part:
        first_sub_parts = [p for p in first_part.split("-", 1) if bool(p)]
        if not first_sub_parts:
            logger.warning(f"Could not get last name from {text}")
            return text

        first_part = first_sub_parts[0]

    return first_part


def _extract_other_names(text: str) -> str:
    match text[1]:
        case _ if text[1].isalpha():
            result = " " + text[1:]
        case " ":
            if text[2] in LAST_NAME_PLACEHOLDERS:
                result = text[2:]
            else:
                result = text[1:]
        case _:
            result = text[1:]

    return result


def _is_valid_next_last_name(current: str, name_range: NameRange) -> bool:
    current = prepare_str_for_comparison(current)
    start = prepare_str_for_comparison(name_range.start)
    end = prepare_str_for_comparison(name_range.end)

    current = _find_last_name_in_str(current)

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

    if all_names.startswith(LAST_NAME_PLACEHOLDERS):
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

    if all_names.startswith(LAST_NAME_PLACEHOLDERS):
        all_names = current_last_name + _extract_other_names(all_names)
    elif all_names.startswith("("):
        all_names = current_last_name + " " + all_names

    return all_names, current_last_name, previous_last_name
