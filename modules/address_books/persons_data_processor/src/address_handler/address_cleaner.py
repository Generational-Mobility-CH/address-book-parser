import re

from modules.address_books.persons_data_processor.src.models.person.address import (
    Address,
)

STREET_NAME_AND_NUMBER = re.compile(
    r"(\d+[a-z]?)\s*([.a-zA-ZäöüÄÖÜ]*)"
)  # TODO: maybe correct regex here to fix #57
LEADING_WHITESPACE_AND_PARENTHESIS_CONTENT = re.compile(r"\s*\(.*\)\s*")


def clean_address(address: Address) -> Address:
    street_name = address.street_name
    street_name = re.sub(LEADING_WHITESPACE_AND_PARENTHESIS_CONTENT, "", street_name)

    if not street_name or street_name.startswith("."):
        street_name = street_name + address.house_number
        street_name = street_name.lstrip(".")

        matches = STREET_NAME_AND_NUMBER.findall(street_name)

        if matches:
            first_group, second_group = matches[0]
            first_group_starts_with_number = first_group[0:1:].isnumeric()

            return Address(
                street_name=second_group
                if first_group_starts_with_number
                else first_group,
                house_number=first_group
                if first_group_starts_with_number
                else second_group,
            )

    address.street_name = street_name

    return address
