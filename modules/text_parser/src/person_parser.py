from modules.shared.models.address import Address
from modules.shared.models.address_book.address_book_entry import AddressBookEntry

from modules.shared.models.person_data_parts import (
    PersonDataParts,
)
from modules.text_parser.src.address_parser import (
    is_address,
    extract_address,
)
from modules.text_parser.src.constants.last_name_placeholders import (
    LAST_NAME_PLACEHOLDERS,
)
from modules.shared.constants.tags import TAG_NONE_FOUND, TAG_NO_JOB


def _is_name(text: str, last_name: str) -> bool:
    return last_name in text or any(
        placeholder in text for placeholder in LAST_NAME_PLACEHOLDERS
    )


def parse_person(data: PersonDataParts, current_last_name: str) -> AddressBookEntry:
    person: AddressBookEntry = AddressBookEntry(
        original_names=TAG_NONE_FOUND,
        address=Address(street_name=TAG_NONE_FOUND, house_number=TAG_NONE_FOUND),
        job=TAG_NO_JOB,
        original_entry=f"{data.first}, {data.second}, {data.third}",
    )

    if (all_names := data.first) and _is_name(all_names, current_last_name):
        person.original_names = all_names

    if len(data) == 2:
        is_address(data.second) and setattr(
            person, "address", extract_address(data.second)
        )
    elif len(data) == 3:
        is_address(data.third) and setattr(
            person, "address", extract_address(data.third)
        )
        person.job = data.second

    return person
