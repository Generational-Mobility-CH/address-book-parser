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


def parse_person(data: PersonDataParts, current_surname: str) -> Person:
    person: Person = Person(
        original_names=TAG_NONE_FOUND,
        address=Address(street_name=TAG_NONE_FOUND, house_number=TAG_NONE_FOUND),
        job=TAG_NO_JOB,
    )

    for e in data:
        if is_name(e, current_surname):
            person.original_names = e
        elif is_address(e):
            person.address = extract_address(e)
        else:
            person.job = e  # TODO: implement is_job() -> bool

    if person.original_names != TAG_NONE_FOUND:
        separated_names = separate_names(person.original_names)
        person.last_names = separated_names.last_names
        person.first_names = separated_names.first_names

    return person


def is_widow(content: PersonDataParts) -> bool:
    return any(item.lower().__contains__(PLACEHOLDER_WIDOW) for item in content)
