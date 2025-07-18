import re

from modules.persons.src.models.pattern_and_replacement import PatternAndReplacement
from modules.persons.src.models.person.address import Address


REPLACE_DOT_AT_STRING_START = re.compile(r"^.\s*")
STREET_NAME_AND_NUMBER = re.compile(r"(\d+[a-z]?)\s*([.a-zA-ZäöüÄÖÜ]*)")


PATS = [PatternAndReplacement(REPLACE_DOT_AT_STRING_START, "")]


def clean_address(address: Address) -> Address:
    street_name = address.street_name

    if street_name.startswith("."):
        street_name = street_name + address.house_number
        street_name = REPLACE_DOT_AT_STRING_START.sub("", street_name)

        matches = re.findall(STREET_NAME_AND_NUMBER, street_name)
        if matches:
            first_element = matches[0]
            if len(first_element) == 2:
                a = first_element[0]
                b = first_element[1]
                if a[0:1:].isnumeric():
                    house_nr = a
                    street_name = b
                else:
                    house_nr = b
                    street_name = a

                return Address(street_name=street_name, house_number=house_nr)

    return address
