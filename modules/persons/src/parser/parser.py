from itertools import chain

from modules.persons.src.models.address_book.addressBook import AddressBook
from modules.persons.src.models.address_book.addressBookPage import AddressBookPage
from modules.persons.src.models.person.person import Person
from modules.persons.src.parser.company_parser import is_company
from modules.persons.src.parser.names.names_parser import (
    starts_with_surname_placeholder,
    is_valid_next_surname_legacy,
    parse_surname,
    extract_other_names,
    get_next_surname,
)
from modules.persons.src.parser.names.special_last_names_parser import (
    handle_special_last_names_if_present,
)
from modules.persons.src.parser.person_parser import parse_person, is_widow
from modules.persons.src.parser.text_sanitizer import (
    clean_text_columns_and_split_into_lines,
)


def parse_address_book(address_book: AddressBook) -> list[Person]:
    persons_collection: list[Person] = []

    for page in address_book.pages:
        persons_collection.extend(parse_address_book_page(page))

    for person in persons_collection:
        person.year = address_book.year

    return persons_collection


def parse_address_book_page(page: AddressBookPage) -> list[Person]:
    page = clean_text_columns_and_split_into_lines(page)
    text = chain.from_iterable(page.text_columns.values())
    grouped_information = group_data(text)
    persons = parse_persons(grouped_information, page)

    for p in persons:
        p.pdf_page_number = page.pdf_page_number

    return persons


def parse_persons(
    grouped_information: list[list[str]], page: AddressBookPage
) -> list[Person]:
    output = []
    current_surname = ""
    previous_surname = ""
    # TODO: add check to see if name range makes sense, e.g.: ["Montmollin", "Dettwiler"] (should be "de montmollin")
    no_name_range = not page.surname_range or len(page.surname_range) != 2

    for group in grouped_information:
        if is_company(group):
            continue

        names = handle_special_last_names_if_present(group[0])

        if len(group) == 2 and is_widow(group):
            if no_name_range:
                group[0], current_surname, previous_surname = parse_legacy(
                    names, current_surname, previous_surname
                )
            else:
                group[0], current_surname = get_next_surname(
                    names, current_surname, page.surname_range
                )
            output.append(parse_person(group, current_surname))
        elif len(group) == 3:
            if no_name_range:
                group[0], current_surname, previous_surname = parse_legacy(
                    names, current_surname, previous_surname
                )
            else:
                group[0], current_surname = get_next_surname(
                    names, current_surname, page.surname_range
                )
            output.append(parse_person(group, current_surname))

    return output


def parse_legacy(
    all_names: str, current_surname: str, previous_surname: str
) -> tuple[str, str, str]:
    if starts_with_surname_placeholder(all_names):
        all_names = current_surname + extract_other_names(all_names)
    elif not current_surname and not previous_surname:
        previous_surname = current_surname = parse_surname(all_names)
    elif is_valid_next_surname_legacy(all_names, previous_surname):
        previous_surname, current_surname = current_surname, parse_surname(all_names)

    return all_names, current_surname, previous_surname


def group_data(text: list[str]) -> list[list[str]]:
    """
    Separate each string into substrings containing information bits.
    Afterward these information bits will be checked and parsed into:
    Names, address, job
    """
    result = []

    for line in text:
        content = line.split(",")
        striped_content = [e for element in content if (e := element.strip())]

        if len(striped_content) in (2, 3):
            result.append(striped_content)

    return result
