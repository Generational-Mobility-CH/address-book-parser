from logging import getLogger

from modules.persons.src.common.special_chars import (
    SPECIAL_NAME_RANGE_LETTERS,
    GERMAN_VOWELS,
)
from modules.persons.src.models.address_book.address_book import AddressBook
from modules.persons.src.models.address_book.address_book_page import AddressBookPage
from modules.persons.src.models.person.person_data_parts import PersonDataParts
from modules.persons.src.models.address_book.name_range import NameRange
from modules.persons.src.models.person.person import Person
from modules.persons.src.parser.company_parser import is_company
from modules.persons.src.parser.names.names_parser import (
    starts_with_surname_placeholder,
    is_valid_next_surname_legacy,
    parse_surname,
    extract_other_names,
    get_next_surname_in_range,
    prepare_str_for_comparison,
)
from modules.persons.src.parser.names.special_last_names_parser import (
    find_special_last_name_keyword,
    handle_special_last_names,
)
from modules.persons.src.parser.person_parser import parse_person, is_widow
from modules.persons.src.parser.text_sanitizer import (
    clean_text_lines,
)


logger = getLogger(__name__)


def parse_address_book(address_book: AddressBook) -> list[Person]:
    persons_collection: list[Person] = []

    if len(address_book.pages) < 1:
        logger.warning(f"No pages found. Skipping book for year {address_book.year}.")
        return persons_collection

    pages_collection = address_book.pages
    first_page = address_book.pages[0]

    first_page.surname_range = NameRange(
        start="A", end=get_next_valid_name_range(pages_collection, 1)
    )

    persons_collection.extend(parse_address_book_page(first_page))

    for page_index, page in enumerate(pages_collection, start=1):
        if not is_valid_surname_range(page.surname_range):
            if starts_with_i_or_j_and_vowel(page.surname_range):
                new_range = NameRange(start="H", end="K")
            else:
                new_range = NameRange(
                    start=get_next_valid_name_range(
                        pages_collection, page_index - 1, -1
                    ),
                    end=get_next_valid_name_range(pages_collection, page_index + 1),
                )

            if is_valid_surname_range(new_range):
                page.surname_range = new_range
            else:
                logger.error(
                    f"Could not approximate 'NameRange' for {address_book.year}-page_{page.pdf_page_number}"
                )

        persons_collection.extend(parse_address_book_page(page))

    return persons_collection


def parse_address_book_page(page: AddressBookPage) -> list[Person]:
    splitted_lines = [line for text in page.text_content for line in text.split("\n")]
    cleaned_lines = clean_text_lines(splitted_lines)
    page.text_content = cleaned_lines

    return parse_persons(page)


def parse_persons(page: AddressBookPage) -> list[Person]:
    output = []
    current_surname = ""
    previous_surname = ""
    grouped_information = group_data(page.text_content)
    has_valid_surname_range = is_valid_surname_range(page.surname_range)

    for group in grouped_information:
        if is_company(group):
            continue

        if special_last_name_keyword := find_special_last_name_keyword(group.first):
            group.first = handle_special_last_names(
                group.first, special_last_name_keyword
            )

        if len(group) == 3 or (len(group) == 2 and is_widow(group)):
            if has_valid_surname_range:
                group.first, current_surname = get_next_surname_in_range(
                    group.first, current_surname, page.surname_range
                )
            else:
                group.first, current_surname, previous_surname = get_next_surname(
                    group.first, current_surname, previous_surname
                )

            person = parse_person(group, current_surname)
            person.year = page.year
            person.pdf_page_number = page.pdf_page_number

            output.append(person)

    return output


def is_valid_surname_range(name_range: NameRange) -> bool:
    has_correct_length = bool(name_range) and len(name_range) == 2
    start = prepare_str_for_comparison(name_range.start)
    end = prepare_str_for_comparison(name_range.end)

    return has_correct_length and start <= end


def starts_with_i_or_j_and_vowel(name_range: NameRange) -> bool:
    """
    Because of linguistic reasons ranges like these or similar are OK:
    ["Itin", "Jungck"] or ["Jenny", "Iffenthaler"]
    (this is the way they are written in the original address book).
    """
    start = name_range.start
    end = name_range.end

    if len(start) < 2 or len(end) < 2:
        logger.error(
            f"Could not compare '{start}' and '{end}' to see if name range is valid."
        )
        return False

    if (
        start[0].lower() in SPECIAL_NAME_RANGE_LETTERS
        and end[0].lower() in SPECIAL_NAME_RANGE_LETTERS
    ):
        if start[1].lower() in GERMAN_VOWELS or end[1].lower() in GERMAN_VOWELS:
            return True

    return False


def get_next_valid_name_range(
    collection: list[AddressBookPage], start: int, direction: int = 1
) -> str:
    result = ""
    end = len(collection) if direction == 1 else -1

    for i in range(start, end, direction):
        name_range = collection[i].surname_range
        if is_valid_surname_range(name_range):
            return name_range.start if direction == 1 else name_range.end

    return result


def get_next_surname(
    all_names: str, current_surname: str, previous_surname: str
) -> tuple[str, str, str]:
    if starts_with_surname_placeholder(all_names):
        all_names = current_surname + extract_other_names(all_names)
    elif not current_surname and not previous_surname:
        previous_surname = current_surname = parse_surname(all_names)
    elif is_valid_next_surname_legacy(all_names, previous_surname):
        previous_surname, current_surname = current_surname, parse_surname(all_names)

    return all_names, current_surname, previous_surname


def group_data(data: list[str]) -> list[PersonDataParts]:
    result: list[PersonDataParts] = []

    for line in data:
        content = line.split(",")
        striped_content = [e for element in content if (e := element.strip())]

        if len(striped_content) in (2, 3):
            result.append(PersonDataParts.from_list(striped_content))

    return result
