import re

from modules.persons.src.models.person.address import Address


STREET_NAME_AND_NUMBER = re.compile(r"(\d+[a-z]?)\s*([.a-zA-ZäöüÄÖÜ]*)")


def clean_address(address: Address) -> Address:
    street_name = address.street_name

    if street_name.startswith("."):
        street_name = street_name + address.house_number
        street_name = street_name.lstrip(".")
        matches = re.findall(STREET_NAME_AND_NUMBER, street_name)

        if matches:
            first, second = matches[0]
            first_starts_with_number = first[0:1:].isnumeric()

            return Address(
                street_name=second if first_starts_with_number else first,
                house_number=first if first_starts_with_number else second,
            )

    return address
