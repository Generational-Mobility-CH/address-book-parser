from modules.persons.src.common.special_chars import (
    TAG_NONE_FOUND,
    TAG_NO_JOB,
    PLACEHOLDER_WIDOW,
)
from modules.persons.src.models.person.person_data_parts import PersonDataParts
from modules.persons.src.models.person.address import Address
from modules.persons.src.models.person.person import Person
from modules.persons.src.parser.address_parser import is_address, extract_address
from modules.persons.src.parser.names.names_parser import is_name
from modules.persons.src.parser.names.names_separator import separate_names


def parse_person(data: PersonDataParts, current_last_name: str) -> Person:
    person: Person = Person(
        original_names=TAG_NONE_FOUND,
        address=Address(street_name=TAG_NONE_FOUND, house_number=TAG_NONE_FOUND),
        job=TAG_NO_JOB,
    )

    if (name := data.first) and is_name(name, current_last_name):
        person.original_names = name
        separated_names = separate_names(person.original_names)
        person.last_names = separated_names.last_names
        person.first_names = separated_names.first_names

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


def is_widow(content: PersonDataParts) -> bool:
    return any(item.lower().__contains__(PLACEHOLDER_WIDOW) for item in content)
