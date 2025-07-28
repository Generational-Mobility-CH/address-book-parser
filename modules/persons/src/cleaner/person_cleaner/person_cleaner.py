from modules.persons.src.cleaner.person_cleaner.address_cleaner import clean_address
from modules.persons.src.cleaner.person_cleaner.first_names_cleaner import (
    clean_first_names,
)
from modules.persons.src.models.person.person import Person
from modules.persons.src.models.person.person_names import PersonNames


def clean_person(person: Person) -> Person:
    cleaned_names = clean_first_names(
        PersonNames(person.first_names, person.last_names)
    )
    person.first_names, person.last_names = (
        cleaned_names.first_names,
        cleaned_names.last_names,
    )

    person.address = clean_address(person.address)

    return person
