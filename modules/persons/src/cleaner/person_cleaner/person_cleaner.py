from modules.persons.src.cleaner.person_cleaner.first_names_cleaner import (
    clean_first_names,
)
from modules.persons.src.cleaner.person_cleaner.last_names_cleaner import (
    clean_last_names,
)
from modules.persons.src.models.person.person import Person
from modules.persons.src.models.person.person_names import PersonNames


def clean_person(person: Person) -> Person:
    all_names = PersonNames(person.first_names, person.last_names)

    all_names = clean_last_names(all_names)
    all_names = clean_first_names(all_names)

    person.first_names = all_names.first_names
    person.last_names = all_names.last_names

    return person
