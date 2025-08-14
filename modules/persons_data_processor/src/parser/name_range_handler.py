from modules.persons_data_processor.src.models.address_book.address_book_page import (
    AddressBookPage,
)
from modules.persons_data_processor.src.models.address_book.name_range import (
    NameRange,
)
from modules.shared.utility.prepare_str_for_comparison import prepare_str_for_comparison


NAME_RANGE_FOR_I_J = NameRange("H", "K")


def _starts_with_i_or_j_and_vowel(name_range: NameRange) -> bool:
    """
    Info: Because of linguistic reasons ranges like these or similar are OK:
    ["Itin", "Jungck"] or ["Jenny", "Iffenthaler"]
    (this is the way they are written in the original address book).
    """
    german_vowels = set("aeiouäöü")
    start = name_range.start
    end = name_range.end

    if len(start) < 2 or len(end) < 2:
        return False

    if start[0].lower() in set("ij") and end[0].lower() in set("ij"):
        if start[1].lower() in german_vowels or end[1].lower() in german_vowels:
            return True

    return False


def is_valid_last_name_range(name_range: NameRange) -> bool:
    if not bool(name_range) or len(name_range) != 2:
        return False

    start = prepare_str_for_comparison(name_range.start)
    end = prepare_str_for_comparison(name_range.end)

    return start <= end


def find_next_valid_name_range(
    collection: list[AddressBookPage], page_index: int
) -> NameRange | None:
    """
    Info: Go a maximum of 3 pages back/forward in order to find a new valid range.
    A broader range does not bring additional benefits for this application.
    """
    if _starts_with_i_or_j_and_vowel(collection[page_index].last_names_range):
        return NAME_RANGE_FOR_I_J

    s_i = page_index
    e_i = page_index

    for i in range(3):
        s_i -= 1
        e_i += 1

        if 0 <= s_i < len(collection) and 0 <= e_i < len(collection):
            start_range = collection[s_i].last_names_range
            end_range = collection[e_i].last_names_range

            new_range = NameRange(
                start=collection[s_i].last_names_range.end.strip(),
                end=collection[e_i].last_names_range.start.strip(),
            )

            if is_valid_last_name_range(start_range) and is_valid_last_name_range(
                end_range
            ):
                return new_range
            elif _starts_with_i_or_j_and_vowel(new_range):
                return NameRange("H", "K")

    return None


def find_next_valid_name_range_start_or_end(
    collection: list[AddressBookPage], start: int, direction: int = 1
) -> str:
    result = ""
    end = len(collection) if direction == 1 else -1

    for i in range(start, end, direction):
        name_range = collection[i].last_names_range

        if is_valid_last_name_range(name_range):
            return name_range.start if direction == 1 else name_range.end

    return result
