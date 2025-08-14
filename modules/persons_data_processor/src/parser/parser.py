from logging import getLogger

from modules.persons_data_processor.src.text_cleaner.text_cleaner import (
    clean_text,
)
from modules.persons_data_processor.src.models.address_book.address_book import (
    AddressBook,
)
from modules.persons_data_processor.src.models.address_book.address_book_page import (
    AddressBookPage,
)
from modules.persons_data_processor.src.models.address_book.name_range import (
    NameRange,
)
from modules.persons_data_processor.src.models.person.person import Person
from modules.persons_data_processor.src.models.person.person_data_parts import (
    PersonDataParts,
)
from modules.persons_data_processor.src.parser.company_parser import (
    is_company,
)
from modules.persons_data_processor.src.parser.last_name_parser import (
    get_next_last_name,
    get_next_last_name_without_range,
)
from modules.persons_data_processor.src.parser.name_range_handler import (
    is_valid_last_name_range,
    find_next_valid_name_range_start_or_end,
    find_next_valid_name_range,
)
from modules.persons_data_processor.src.parser.person_parser import (
    parse_person,
)

logger = getLogger(__name__)


def _group_data(data: list[str]) -> list[PersonDataParts]:
    result: list[PersonDataParts] = []

    for line in data:
        content = line.split(",")
        stripped_content = []
        for e in content:
            e = e.strip()
            if e and any(char.isalnum() for char in e):
                stripped_content.append(e)

        if len(stripped_content) in (2, 3):
            result.append(PersonDataParts.from_list(stripped_content))

    return result


def _parse_address_book_page(page: AddressBookPage) -> list[Person]:
    splitted_lines = [line for text in page.text_content for line in text.split("\n")]
    cleaned_lines = clean_text(splitted_lines)
    page.text_content = cleaned_lines

    return _parse_persons(page)


def _parse_persons(page: AddressBookPage) -> list[Person]:
    output = []
    current_last_name = ""
    previous_last_name = ""
    grouped_information = _group_data(page.text_content)
    has_valid_last_names_range = is_valid_last_name_range(page.last_names_range)

    for group in grouped_information:
        if is_company(group):
            continue

        if len(group) in (2, 3):
            if has_valid_last_names_range:
                group.first, current_last_name = get_next_last_name(
                    group.first, current_last_name, page.last_names_range
                )
            else:
                group.first, current_last_name, previous_last_name = (
                    get_next_last_name_without_range(
                        group.first, current_last_name, previous_last_name
                    )
                )

            person = parse_person(group, current_last_name)
            person.year = page.year
            person.pdf_page_number = page.pdf_page_number

            if person not in output:
                output.append(person)

    return output


def parse_address_book(address_book: AddressBook) -> list[Person]:
    persons_collection: list[Person] = []

    if len(address_book.pages) < 1:
        logger.warning(f"No pages found. Skipping book for year {address_book.year}.")
        return persons_collection

    pages_collection = address_book.pages
    first_page = address_book.pages[0]

    first_page.last_names_range = NameRange(
        start="A", end=find_next_valid_name_range_start_or_end(pages_collection, 1)
    )

    persons_collection.extend(_parse_address_book_page(first_page))

    for page_index in range(1, len(pages_collection)):
        page = address_book.pages[page_index]
        logger.debug(f"Parsing page {page.pdf_page_number} from year {page.year}...")

        if not is_valid_last_name_range(page.last_names_range):
            if found_next_valid_range := find_next_valid_name_range(
                pages_collection, page_index
            ):
                page.last_names_range = found_next_valid_range
            else:
                logger.warning(
                    f"Could not approximate 'NameRange' for {address_book.year}-page_{page.pdf_page_number}"
                )

        persons_collection.extend(_parse_address_book_page(page))

    return persons_collection
