import logging

from modules.persons.common.special_chars import PLACEHOLDERS_SURNAME


GERMAN_UMLAUTE = {"ä": "a", "ö": "o", "ü": "u"}


def extract_other_names(text: str) -> str:
    match text[1]:
        case _ if text[1].isalpha():
            result = " " + text[1:]
        case " ":
            if text[2] in PLACEHOLDERS_SURNAME:
                result = text[2:]
            else:
                result = text[1:]
        case _:
            result = text[1:]

    return result


def parse_surname(text: str) -> str:
    return text.split(" ")[0].split("-")[0]


def is_name(text: str, surname: str) -> bool:
    return surname in text or any(
        placeholder in text for placeholder in PLACEHOLDERS_SURNAME
    )


def is_valid_next_surname(current: str, surname_range: list[str]) -> bool:
    if len(surname_range) != 2:
        logging.error(surname_range)
        return True

    current, surname_range[0], surname_range[1] = replace_if_contains_umlaute(
        current, surname_range[0], surname_range[1]
    )

    if surname_range[0].lower() <= current.lower() <= surname_range[1].lower():
        return True

    return False


def contains_umlaute(input_string: str) -> bool:
    return any(char in GERMAN_UMLAUTE for char in input_string.lower())


def replace_umlaute(text: str) -> str:
    return "".join(GERMAN_UMLAUTE.get(char, char) for char in text.lower())


def replace_if_contains_umlaute(*args) -> list[str]:
    return [replace_umlaute(arg) if contains_umlaute(arg) else arg for arg in args]


def starts_with_surname_placeholder(text: str) -> bool:
    return bool(text and text[0] in PLACEHOLDERS_SURNAME)


def is_valid_next_surname_legacy(current: str, previous: str) -> bool:
    """Check if 'current' starts with the same letter as 'previous'
    or if it starts with the next letter in alphabetical order"""

    current, previous = replace_if_contains_umlaute(current, previous)

    if current[0].lower() == previous[0].lower():
        return True
    elif ord(current[0].lower()) == ord(previous[0].lower()) + 1:
        return True

    return False


def get_next_surname(
    all_names: str, current_surname: str, surname_range
) -> tuple[str, str]:
    if starts_with_surname_placeholder(all_names):
        all_names = current_surname + extract_other_names(all_names)
    elif not current_surname:
        current_surname = parse_surname(all_names)
    elif is_valid_next_surname(all_names, surname_range):
        current_surname = parse_surname(all_names)
    else:
        all_names = f"{current_surname} {all_names}"

    return all_names, current_surname
