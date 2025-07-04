from modules.persons.src.common.special_chars import (
    PLACEHOLDERS_SURNAME,
    GERMAN_UMLAUTE,
)
from modules.persons.src.models.address_book.name_range import NameRange


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


def prepare_str_for_comparison(text: str) -> str:
    text = text.strip()
    text = replace_if_contains_umlaute(text)
    text = text.lower()

    return text


def is_valid_next_surname(current: str, surname_range: NameRange) -> bool:
    current = prepare_str_for_comparison(current)
    start = prepare_str_for_comparison(surname_range.start)
    end = prepare_str_for_comparison(surname_range.end)

    return start <= current <= end


def is_valid_next_surname_legacy(current: str, previous: str) -> bool:
    current = prepare_str_for_comparison(current)
    previous = prepare_str_for_comparison(previous)

    if current <= previous:
        return True
    elif ord(current[0]) == ord(previous[0]) + 1:
        return True

    return False


def get_next_surname_given_range(
    all_names: str, current_surname: str, surname_range: NameRange
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


def contains_umlaute(input_string: str) -> bool:
    return any(char in GERMAN_UMLAUTE for char in input_string.lower())


def replace_umlaute(text: str) -> str:
    return "".join(GERMAN_UMLAUTE.get(char, char) for char in text.lower()).title()


def replace_if_contains_umlaute(text: str) -> str:
    return replace_umlaute(text) if contains_umlaute(text) else text


def starts_with_surname_placeholder(text: str) -> bool:
    return bool(text) and text[0] in PLACEHOLDERS_SURNAME
